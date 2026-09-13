"""Connect our OLMo 3 experiment to the public Kronfluence library.

Purpose
-------
This file contains the experiment-specific pieces that Kronfluence cannot know:
how our saved token windows are represented, how the 64 in-context queries are
tokenized, which scalar losses are differentiated, which OLMo 3 modules are
tracked, and which EK-FAC settings reproduce the Ruis et al. methodology.

External inputs
---------------
The classes in this file receive these inputs from ``run_olmo3_kronfluence.py``:

1. ``hessian_tokens.npy``: a NumPy array with shape ``(10_000, 512)`` and
   little-endian ``uint32`` values. Each row is one sampled training window.
2. ``ranking_tokens.npy``: a NumPy array with shape ``(100_000, 512)`` and
   little-endian ``uint32`` values. Each row is one candidate document window.
3. ``strict_matched_queries.jsonl``: 64 JSON objects containing the complete
   in-context prompt and its correct completion.
4. The pinned Hugging Face model ``allenai/Olmo-3-1025-7B`` at the immutable
   stage-one commit declared in ``stage1_data.py``.

Outputs
-------
This module does not itself write result files. It returns:

* PyTorch ``Dataset`` examples represented as ``dict[str, torch.Tensor]``;
* a loaded ``torch.nn.Module`` containing OLMo 3;
* a Kronfluence ``Task`` defining the differentiable losses;
* ``FactorArguments`` and ``ScoreArguments`` configuration objects.

The runner passes those objects to Kronfluence. Kronfluence then writes the
EK-FAC factors and the ``64 x 100_000`` raw influence-score matrix.

Functional dependencies
-----------------------
Factor fitting follows this path::

    hessian_tokens.npy -> TokenWindowDataset
      -> Olmo3LanguageModelingTask.compute_train_loss
      -> factor_arguments -> Analyzer.fit_all_factors

Influence scoring follows this path::

    strict_matched_queries.jsonl -> ConditionalQueryDataset
    ranking_tokens.npy           -> TokenWindowDataset
      -> Olmo3LanguageModelingTask.compute_measurement / compute_train_loss
      -> score_arguments -> Analyzer.compute_pairwise_scores

Both paths depend on ``load_stage_one_model`` and use
``get_influence_tracked_modules`` to restrict attribution to OLMo 3's MLP
projection matrices.
"""

from __future__ import annotations

from importlib.metadata import version
import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from kronfluence.analyzer import Analyzer
from kronfluence.arguments import FactorArguments, ScoreArguments
from kronfluence.task import Task
from torch import nn
from torch.utils.data import Dataset

from stage1_data import (
    ANALYSIS_WINDOW_LENGTH,
    MODEL_COMMIT,
    MODEL_ID,
)


EXPECTED_KRONFLUENCE_VERSION = "1.0.1"
NUM_LAYERS = 32
EXPECTED_HESSIAN_WINDOWS = 10_000
EXPECTED_RANKING_WINDOWS = 100_000
EXPECTED_QUERIES = 64
EXPECTED_PAIRS = 32


# ---------------------------------------------------------------------------
# Dependency-version validation
# ---------------------------------------------------------------------------

def verify_kronfluence_version() -> str:
    """Verify that the expected Kronfluence release is installed.

    Inputs:
        None. The function reads installed-package metadata from the active
        Python environment.

    Returns:
        ``str``: The installed version, which must be ``"1.0.1"``.

    Raises:
        RuntimeError: If a different version is installed.

    Function in the pipeline:
        Kronfluence uses internal APIs that can change across releases. The
        runner calls this before loading data or the 7B model so an incompatible
        environment fails early and cheaply.
    """

    # ``version`` reads package metadata; it does not import or run an analysis.
    installed = version("kronfluence")
    if installed != EXPECTED_KRONFLUENCE_VERSION:
        raise RuntimeError(
            f"Kronfluence {EXPECTED_KRONFLUENCE_VERSION} is required; "
            f"found {installed}"
        )
    return installed


# ---------------------------------------------------------------------------
# Pretraining-window input
# ---------------------------------------------------------------------------

class TokenWindowDataset(Dataset):
    """Expose a saved token matrix through PyTorch's Dataset interface.

    Input type:
        A path to a ``.npy`` matrix and the exact number of rows expected in
        that matrix. Every row contains 512 ``uint32`` OLMo token IDs.

    Output type:
        Indexing the dataset returns ``dict[str, torch.Tensor]`` with
        ``input_ids``, ``attention_mask``, and ``labels``, each having shape
        ``(512,)`` and dtype ``torch.int64``.

    Function in the pipeline:
        Kronfluence expects a PyTorch Dataset. This class adapts our downloaded
        NumPy arrays without loading the entire 20 MB or 205 MB matrix into RAM.
    """

    def __init__(self, path: str | Path, *, expected_rows: int) -> None:
        """Open and validate one Hessian or ranking token matrix.

        Args:
            path: ``str`` or ``Path`` pointing to the ``.npy`` matrix.
            expected_rows: ``int`` specifying the required number of windows;
                10,000 for Hessian fitting or 100,000 for ranking.

        Returns:
            ``None``. The opened memory map is stored in ``self.tokens``.

        Raises:
            ValueError: If the matrix has the wrong shape or dtype.
        """

        self.path = Path(path)
        # ``mmap_mode="r"`` reads individual rows on demand instead of copying
        # the full matrix into process memory.
        self.tokens = np.load(self.path, mmap_mode="r")
        expected_shape = (expected_rows, ANALYSIS_WINDOW_LENGTH)
        # An exact shape check catches partial downloads and swapped cohorts.
        if self.tokens.shape != expected_shape:
            raise ValueError(
                f"{self.path} has shape {self.tokens.shape}; expected {expected_shape}"
            )
        # Dolma 3's pretokenized shards and our downloaded arrays use
        # little-endian unsigned 32-bit token IDs.
        if self.tokens.dtype != np.dtype("<u4"):
            raise ValueError(
                f"{self.path} has dtype {self.tokens.dtype}; expected uint32"
            )

    def __len__(self) -> int:
        """Return the number of 512-token windows as a Python ``int``."""

        return int(self.tokens.shape[0])

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        """Convert one saved token window into a causal-LM training example.

        Args:
            index: Zero-based row index in the NumPy matrix.

        Returns:
            A dictionary containing three ``torch.int64`` tensors of shape
            ``(512,)``:

            * ``input_ids``: tokens supplied to OLMo 3;
            * ``attention_mask``: all ones because these windows have no pad;
            * ``labels``: a copy of ``input_ids`` for next-token prediction.

        Function in the pipeline:
            Kronfluence batches these dictionaries before asking
            ``Olmo3LanguageModelingTask`` for a training loss.
        """

        # Copying detaches the row from the read-only NumPy memory map and
        # converts uint32 IDs into the int64 dtype expected by Transformers.
        input_ids = torch.from_numpy(
            np.array(self.tokens[index], dtype=np.int64, copy=True)
        )
        return {
            "input_ids": input_ids,
            # Every position contains a real token, so every position is visible.
            "attention_mask": torch.ones_like(input_ids),
            # Hugging Face causal LMs conceptually predict the next entry in this
            # same sequence; the shift itself is performed in ``_loss`` below.
            "labels": input_ids.clone(),
        }


# ---------------------------------------------------------------------------
# Query-manifest input and tokenization
# ---------------------------------------------------------------------------

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Read a JSONL file into an ordered list of JSON objects.

    Args:
        path: ``str`` or ``Path`` to the query manifest.

    Returns:
        ``list[dict[str, Any]]`` in exactly the same order as the file.

    Raises:
        ValueError: If a non-empty line contains a JSON value that is not an
        object/dictionary. JSON syntax errors are reported by ``json.loads``.

    Function in the pipeline:
        Preserving order is essential because row ``i`` of the final influence
        matrix must correspond to query ``i`` in this manifest.
    """

    records: list[dict[str, Any]] = []
    with Path(path).open(encoding="utf-8") as file_handle:
        for line_number, line in enumerate(file_handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"line {line_number} is not a JSON object")
            records.append(record)
    return records


def validate_query_records(records: list[dict[str, Any]]) -> None:
    """Validate the frozen 32 composition/shortcut matched pairs.

    Args:
        records: Ordered ``list`` of query dictionaries returned by
        ``read_jsonl``.

    Returns:
        ``None``. Success means all checks passed; the records are not modified.

    Raises:
        ValueError: If query count, order, group, pair membership, task, model,
        correctness, or matched country/capital values differ from the frozen
        experimental cohort.

    Function in the pipeline:
        Prevents influence calculations from silently using incorrect queries
        or mixing a composition query with a shortcut query having a different
        answer.
    """

    # The cohort consists of 32 pairs, hence exactly 64 ordered query records.
    if len(records) != EXPECTED_QUERIES:
        raise ValueError(
            f"expected {EXPECTED_QUERIES} influence queries, found {len(records)}"
        )
    for query_index, record in enumerate(records):
        # Each pair is stored composition first, shortcut second.
        expected_group = "composition" if query_index % 2 == 0 else "shortcut"
        if record.get("query_index") != query_index:
            raise ValueError(f"query {query_index} has a non-contiguous query_index")
        if record.get("pair_index") != query_index // 2:
            raise ValueError(f"query {query_index} has the wrong pair_index")
        if record.get("group") != expected_group:
            raise ValueError(f"query {query_index} is not in group {expected_group!r}")
        if record.get("task") != "landmark_country_capital":
            raise ValueError(f"query {query_index} has the wrong task")
        if record.get("model") != MODEL_ID or record.get("model_commit") != MODEL_COMMIT:
            raise ValueError(f"query {query_index} uses the wrong model checkpoint")
        prompt = record.get("prompt")
        completion = record.get("completion")
        if not isinstance(prompt, str) or not prompt:
            raise ValueError(f"query {query_index} has no prompt")
        if not isinstance(completion, str) or not completion:
            raise ValueError(f"query {query_index} has no completion")
        if record.get("model_prediction") != completion:
            raise ValueError(f"query {query_index} was not answered correctly")

    # Adjacent records must share the same intermediate country and final
    # capital. This controls the answer while comparing predictor types.
    for pair_index in range(EXPECTED_PAIRS):
        composition, shortcut = records[2 * pair_index : 2 * pair_index + 2]
        if (composition.get("country"), composition.get("capital")) != (
            shortcut.get("country"),
            shortcut.get("capital"),
        ):
            raise ValueError(f"pair {pair_index} does not share country and capital")


def encode_conditional_query(
    tokenizer: Any, prompt: str, completion: str
) -> dict[str, torch.Tensor]:
    """Tokenize one prompt/completion and restrict loss to the completion.

    Args:
        tokenizer: A Hugging Face tokenizer exposing ``encode``.
        prompt: ``str`` containing all ten in-context examples and the final
            ``Q: ...\\nA:`` prefix.
        completion: ``str`` containing the known-correct model answer, including
            its leading space (for example, ``" Cairo"``).

    Returns:
        ``dict[str, torch.Tensor]`` containing one-dimensional ``input_ids``,
        ``attention_mask``, and ``labels`` tensors. Prompt labels are ``-100``;
        completion labels retain their token IDs.

    Raises:
        ValueError: If separate prompt tokenization is not a prefix of combined
        tokenization or the completion produces no tokens.

    Function in the pipeline:
        The model sees the entire in-context prompt, but only the correct answer
        contributes to the query gradient used by Kronfluence.
    """

    # Tokenize the exact text the model conditions on. Special tokens are not
    # inserted because the behavioral evaluation used this raw prompt format.
    full_ids = tokenizer.encode(prompt + completion, add_special_tokens=False)
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    # This guard ensures the label mask begins at the actual token boundary
    # between the prompt and completion.
    if full_ids[: len(prompt_ids)] != prompt_ids:
        raise ValueError(
            "prompt token IDs are not a prefix of prompt-plus-completion token IDs"
        )
    if len(full_ids) == len(prompt_ids):
        raise ValueError("completion produced no token IDs")
    # PyTorch cross-entropy ignores labels equal to -100. Thus prompt tokens
    # remain model inputs but make zero direct contribution to the scalar loss.
    labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids) :]
    input_ids = torch.tensor(full_ids, dtype=torch.long)
    return {
        "input_ids": input_ids,
        "attention_mask": torch.ones_like(input_ids),
        "labels": torch.tensor(labels, dtype=torch.long),
    }


class ConditionalQueryDataset(Dataset):
    """Expose the 64 correct in-context completions as a PyTorch Dataset.

    Input type:
        A JSONL path plus the pinned OLMo tokenizer.

    Output type:
        Indexing returns the tensor dictionary created by
        ``encode_conditional_query``. Sequence lengths may differ between
        queries, so the runner uses query batch size one.

    Function in the pipeline:
        Supplies Kronfluence with the 64 query measurements whose gradients are
        compared against the 100,000 ranking-window gradients.
    """

    def __init__(self, path: str | Path, tokenizer: Any) -> None:
        """Read, validate, and tokenize all query records once.

        Args:
            path: ``str`` or ``Path`` to ``strict_matched_queries.jsonl``.
            tokenizer: The tokenizer belonging to the pinned stage-one model.

        Returns:
            ``None``. Raw dictionaries are saved in ``self.records`` and tensor
            examples in ``self.examples``.
        """

        self.path = Path(path)
        self.records = read_jsonl(self.path)
        validate_query_records(self.records)
        self.examples = [
            encode_conditional_query(
                tokenizer,
                prompt=record["prompt"],
                completion=record["completion"],
            )
            for record in self.records
        ]

    def __len__(self) -> int:
        """Return the number of encoded queries (exactly 64 after validation)."""

        return len(self.examples)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        """Return query ``index`` as an encoded tensor dictionary."""

        return self.examples[index]


# ---------------------------------------------------------------------------
# Differentiable losses and tracked OLMo modules
# ---------------------------------------------------------------------------

class Olmo3LanguageModelingTask(Task):
    """Tell Kronfluence what to differentiate and which weights to attribute.

    Input type:
        Batches are dictionaries of two-dimensional tensors with shape
        ``(batch_size, sequence_length)``. The model is an OLMo causal LM.

    Output type:
        Loss methods return one scalar ``torch.Tensor`` so ``backward()`` can
        produce gradients.

    Function in the pipeline:
        Kronfluence is model-agnostic. This task supplies the training-document
        and query objectives and restricts tracking to 96 MLP projections
        (three projections in each of 32 transformer layers), following the
        Ruis et al. approximation.
    """

    @staticmethod
    def _loss(
        batch: dict[str, torch.Tensor],
        model: nn.Module,
        *,
        sample: bool,
    ) -> torch.Tensor:
        """Calculate summed next-token negative log-likelihood.

        Args:
            batch: Tensor dictionary containing ``input_ids``,
                ``attention_mask``, and ``labels``.
            model: OLMo 3, or a compatible causal language model.
            sample: If ``False``, score the supplied labels. If ``True``, sample
                labels from the model distribution for the true-Fisher Monte
                Carlo approximation used while fitting EK-FAC factors.

        Returns:
            A scalar ``torch.Tensor`` equal to the sum of cross-entropy over all
            non-masked next-token labels.

        Function in the pipeline:
            Both Hessian estimation and influence scoring ultimately depend on
            gradients of this scalar with respect to tracked MLP weights.
        """

        # The forward pass returns one vocabulary-logit vector per input token.
        logits = model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        ).logits
        # A causal LM uses logits at position t to predict the label at t + 1.
        # The final logit has no following label, and the first label has no
        # preceding logit, so the two tensors are shifted by one position.
        shifted_logits = logits[..., :-1, :].contiguous()
        shifted_labels = batch["labels"][..., 1:].contiguous()

        if sample:
            # Kronfluence requests sampled labels while estimating a true
            # Fisher/Gauss-Newton curvature matrix. Sampling is detached so the
            # random targets themselves do not become part of the gradient.
            with torch.no_grad():
                probabilities = torch.softmax(
                    shifted_logits.detach().float(), dim=-1
                )
                labels = torch.multinomial(
                    probabilities.view(-1, probabilities.shape[-1]),
                    num_samples=1,
                ).view_as(shifted_labels)
                labels.masked_fill_(shifted_labels == -100, -100)
        else:
            labels = shifted_labels

        # ``reduction="sum"`` treats each window as one document-level loss and
        # matches Kronfluence's official language-model example.
        return F.cross_entropy(
            shifted_logits.view(-1, shifted_logits.shape[-1]).float(),
            labels.view(-1),
            reduction="sum",
            ignore_index=-100,
        )

    def compute_train_loss(
        self,
        batch: dict[str, torch.Tensor],
        model: nn.Module,
        sample: bool = False,
    ) -> torch.Tensor:
        """Return the document loss requested by Kronfluence.

        Args:
            batch: Batched Hessian or ranking-window tensor dictionary.
            model: The prepared OLMo 3 model.
            sample: Kronfluence sets this to ``True`` during true-Fisher factor
                fitting and ``False`` for actual ranking documents.

        Returns:
            Scalar summed next-token negative log-likelihood.
        """

        return self._loss(batch, model, sample=sample)

    def compute_measurement(
        self,
        batch: dict[str, torch.Tensor],
        model: nn.Module,
    ) -> torch.Tensor:
        """Return the query quantity whose training-data influence we measure.

        Args:
            batch: A batched conditional query from
                ``ConditionalQueryDataset``.
            model: The prepared OLMo 3 model.

        Returns:
            Scalar negative log-likelihood of only the correct completion. The
            prompt labels are ``-100`` and therefore ignored.

        Function in the pipeline:
            Kronfluence differentiates this value to obtain the query gradient.
            Combined with the document-loss gradient and inverse curvature, it
            yields each query-document influence score.
        """

        return self._loss(batch, model, sample=False)

    def get_influence_tracked_modules(self) -> list[str]:
        """Return the exact OLMo 3 module names Kronfluence should wrap.

        Inputs:
            None; module names follow the fixed 32-layer OLMo 3 architecture.

        Returns:
            ``list[str]`` of length 96: ``gate_proj``, ``up_proj``, and
            ``down_proj`` for every transformer MLP layer.

        Function in the pipeline:
            Excludes embeddings, the LM head, and attention projections from
            factor fitting and influence scoring.
        """

        names: list[str] = []
        for layer in range(NUM_LAYERS):
            for projection in ("gate_proj", "up_proj", "down_proj"):
                names.append(f"model.layers.{layer}.mlp.{projection}")
        return names

    def get_attention_mask(
        self, batch: dict[str, torch.Tensor]
    ) -> torch.Tensor:
        """Give Kronfluence the mask corresponding to the current batch.

        Args:
            batch: Tensor dictionary containing ``attention_mask``.

        Returns:
            A ``torch.Tensor`` with one for each real token. Our examples use no
            padding, but exposing this mask satisfies Kronfluence's transformer
            interface and prevents future padded positions from being counted.
        """

        return batch["attention_mask"]


# ---------------------------------------------------------------------------
# Pinned model loading and architecture validation
# ---------------------------------------------------------------------------

def load_stage_one_model(*, gradient_checkpointing: bool = True) -> nn.Module:
    """Load the exact OLMo 3 stage-one checkpoint for gradient computation.

    Args:
        gradient_checkpointing: ``bool`` controlling whether intermediate
            activations are recomputed during backward passes to reduce memory.

    Returns:
        ``torch.nn.Module``: The pinned OLMo 3 causal language model in eval
        mode, with bfloat16 weights and generation caching disabled.

    Function in the pipeline:
        Both factor fitting and scoring must differentiate the same immutable
        stage-one model used for the behavioral and logit-lens experiments.
        Device placement is intentionally left to Kronfluence/Accelerate.
    """

    from transformers import AutoModelForCausalLM

    # The immutable commit prevents a moving branch or tag from changing the
    # weights, configuration, or architecture in a later run.
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )
    # Key/value generation caches are useful for decoding but incompatible with
    # the full-sequence backward passes required here.
    model.config.use_cache = False
    if gradient_checkpointing:
        model.gradient_checkpointing_enable(
            gradient_checkpointing_kwargs={"use_reentrant": False}
        )
    model.eval()
    return model


def validate_tracked_modules(model: nn.Module, task: Olmo3LanguageModelingTask) -> None:
    """Check that every requested MLP projection exists in the loaded model.

    Args:
        model: Loaded OLMo 3 ``torch.nn.Module``.
        task: ``Olmo3LanguageModelingTask`` defining the 96 expected names.

    Returns:
        ``None``; the model and task are not modified.

    Raises:
        ValueError: If the architecture does not contain any requested module.

    Function in the pipeline:
        Detects an incorrect checkpoint or Transformers architecture before the
        expensive factor-fitting pass begins.
    """

    available = dict(model.named_modules())
    missing = [
        name for name in task.get_influence_tracked_modules() if name not in available
    ]
    if missing:
        raise ValueError(f"OLMo 3 is missing tracked MLP modules: {missing[:3]}")


# ---------------------------------------------------------------------------
# Kronfluence 1.0.1 compatibility
# ---------------------------------------------------------------------------

def restore_torch_dtype(value: Any) -> Any:
    """Convert a serialized dtype name back into a ``torch.dtype`` object.

    Args:
        value: Any value read from Kronfluence's factor-arguments JSON.

    Returns:
        The matching ``torch.dtype`` for strings such as ``"torch.bfloat16"``;
        otherwise the original value unchanged.

    Function in the pipeline:
        Factor fitting and scoring are separate processes. Kronfluence 1.0.1
        serializes dtypes as strings but omits the reverse conversion when it
        reloads factors, so this restores the types required by ``Tensor.to``.
    """

    if isinstance(value, str) and value.startswith("torch."):
        candidate = getattr(torch, value.removeprefix("torch."), None)
        if isinstance(candidate, torch.dtype):
            return candidate
    return value


class DtypeSafeAnalyzer(Analyzer):
    """Kronfluence Analyzer with localized dtype restoration.

    This subclass changes only factor-argument loading. All EK-FAC estimation
    and pairwise-score calculations remain Kronfluence's implementation.
    """

    def load_factor_args(self, factors_name: str) -> FactorArguments | None:
        """Load saved factor settings and restore serialized torch dtypes.

        Args:
            factors_name: ``str`` identifying the saved factor directory.

        Returns:
            ``FactorArguments`` with real dtype objects, or ``None`` if the
            requested factors do not have saved arguments.

        Function in the pipeline:
            Called internally by Kronfluence when scoring reloads factors made
            by an earlier ``fit-factors`` process.
        """

        arguments = super().load_factor_args(factors_name)
        if arguments is not None:
            for name, value in vars(arguments).items():
                setattr(arguments, name, restore_torch_dtype(value))
        return arguments


# ---------------------------------------------------------------------------
# EK-FAC factor and pairwise-score configuration
# ---------------------------------------------------------------------------

def factor_arguments(
    *, covariance_module_partitions: int = 2, lambda_module_partitions: int = 4
) -> FactorArguments:
    """Construct EK-FAC settings for the 10,000-window Hessian pilot.

    Args:
        covariance_module_partitions: Number of groups in which Kronfluence
            processes tracked modules while estimating covariance matrices.
        lambda_module_partitions: Number of module groups used while estimating
            EK-FAC's corrected eigenvalues (Lambda matrices).

    Returns:
        ``FactorArguments`` passed directly to ``Analyzer.fit_all_factors``.

    Function in the pipeline:
        Requests EK-FAC with a sampled-label true Fisher, uses every available
        Hessian window, and chooses bfloat16 storage plus CPU offloading to make
        the 7B analysis tractable. The separate two-block eigendecomposition is
        installed by ``kronfluence_block_diagonal.py`` in the runner.
    """

    return FactorArguments(
        strategy="ekfac",
        use_empirical_fisher=False,
        amp_dtype=torch.bfloat16,
        covariance_max_examples=None,
        covariance_data_partitions=4,
        covariance_module_partitions=covariance_module_partitions,
        activation_covariance_dtype=torch.bfloat16,
        gradient_covariance_dtype=torch.bfloat16,
        eigendecomposition_dtype=torch.float64,
        lambda_max_examples=None,
        lambda_data_partitions=4,
        lambda_module_partitions=lambda_module_partitions,
        use_iterative_lambda_aggregation=True,
        offload_activations_to_cpu=True,
        per_sample_gradient_dtype=torch.bfloat16,
        lambda_dtype=torch.bfloat16,
    )


def score_arguments(
    *, query_count: int, data_partitions: int = 10, module_partitions: int = 4
) -> ScoreArguments:
    """Construct settings for the 64-by-100,000 influence calculation.

    Args:
        query_count: Number of query gradients accumulated together; 64 here.
        data_partitions: Number of chunks used to process/save ranking windows.
        module_partitions: Number of chunks used to process tracked MLP modules.

    Returns:
        ``ScoreArguments`` passed directly to
        ``Analyzer.compute_pairwise_scores``.

    Function in the pipeline:
        Applies Ruis et al.'s damping value of 0.1 and compresses the 64 query
        gradients to rank 32 so the ranking windows need only be traversed once
        per partition. Scores are accumulated across all tracked MLP modules and
        stored as float32 document-level values, not token-level values.
    """

    return ScoreArguments(
        damping_factor=0.1,
        amp_dtype=torch.bfloat16,
        offload_activations_to_cpu=True,
        data_partitions=data_partitions,
        module_partitions=module_partitions,
        compute_per_module_scores=False,
        compute_per_token_scores=False,
        query_gradient_accumulation_steps=query_count,
        query_gradient_low_rank=min(32, query_count),
        use_full_svd=False,
        query_gradient_svd_dtype=torch.float32,
        per_sample_gradient_dtype=torch.float32,
        precondition_dtype=torch.float32,
        score_dtype=torch.float32,
    )
