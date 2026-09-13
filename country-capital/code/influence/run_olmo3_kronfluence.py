"""Fit OLMo 3 EK-FAC factors or score landmark-country-capital queries."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import torch
from kronfluence.analyzer import prepare_model
from kronfluence.utils.dataset import DataLoaderKwargs
from transformers import AutoTokenizer, default_data_collator

from kronfluence_block_diagonal import install_two_block_eigendecomposition
from olmo3_kronfluence import (
    ConditionalQueryDataset,
    DtypeSafeAnalyzer,
    EXPECTED_HESSIAN_WINDOWS,
    EXPECTED_QUERIES,
    EXPECTED_RANKING_WINDOWS,
    Olmo3LanguageModelingTask,
    TokenWindowDataset,
    factor_arguments,
    load_stage_one_model,
    score_arguments,
    validate_tracked_modules,
    verify_kronfluence_version,
)
from stage1_data import MODEL_COMMIT, MODEL_ID


COUNTRY_CAPITAL_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = COUNTRY_CAPITAL_DIR / "results" / "influence"
DEFAULT_HESSIAN_TOKENS = RESULTS_DIR / "hessian_tokens.npy"
DEFAULT_RANKING_TOKENS = RESULTS_DIR / "ranking_tokens.npy"
DEFAULT_QUERIES = RESULTS_DIR / "strict_matched_queries.jsonl"
DEFAULT_OUTPUT_DIR = RESULTS_DIR / "kronfluence"
ANALYSIS_NAME = "olmo3_stage1_landmark_country_capital"
FACTORS_NAME = "ekfac_mlp_two_block_hessian10k"
SCORES_NAME = "queries64_ranking100k"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="stage", required=True)

    fit = subparsers.add_parser("fit-factors")
    fit.add_argument("--tokens", type=Path, default=DEFAULT_HESSIAN_TOKENS)
    fit.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    fit.add_argument("--batch-size", type=int, default=1)
    fit.add_argument("--workers", type=int, default=2)
    fit.add_argument("--covariance-module-partitions", type=int, default=2)
    fit.add_argument("--lambda-module-partitions", type=int, default=4)
    fit.add_argument("--overwrite", action="store_true")
    fit.add_argument("--no-gradient-checkpointing", action="store_true")

    score = subparsers.add_parser("score")
    score.add_argument("--tokens", type=Path, default=DEFAULT_RANKING_TOKENS)
    score.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    score.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    score.add_argument("--query-batch-size", type=int, default=1)
    score.add_argument("--train-batch-size", type=int, default=1)
    score.add_argument("--workers", type=int, default=2)
    score.add_argument("--data-partitions", type=int, default=10)
    score.add_argument("--module-partitions", type=int, default=4)
    score.add_argument("--overwrite", action="store_true")
    score.add_argument("--no-gradient-checkpointing", action="store_true")
    return parser.parse_args(argv)


def make_analyzer(
    *, output_dir: Path, gradient_checkpointing: bool
) -> tuple[DtypeSafeAnalyzer, Olmo3LanguageModelingTask]:
    task = Olmo3LanguageModelingTask()
    model = load_stage_one_model(gradient_checkpointing=gradient_checkpointing)
    validate_tracked_modules(model, task)
    model = prepare_model(model=model, task=task)
    analyzer = DtypeSafeAnalyzer(
        analysis_name=ANALYSIS_NAME,
        model=model,
        task=task,
        output_dir=str(output_dir),
    )
    return analyzer, task


def dataloader_kwargs(workers: int) -> DataLoaderKwargs:
    if workers < 0:
        raise ValueError("workers cannot be negative")
    return DataLoaderKwargs(
        num_workers=workers,
        collate_fn=default_data_collator,
        pin_memory=True,
    )


def fit_factors(args: argparse.Namespace) -> None:
    dataset = TokenWindowDataset(
        args.tokens, expected_rows=EXPECTED_HESSIAN_WINDOWS
    )
    install_two_block_eigendecomposition()
    analyzer, _ = make_analyzer(
        output_dir=args.output_dir,
        gradient_checkpointing=not args.no_gradient_checkpointing,
    )
    loader = dataloader_kwargs(args.workers)
    analyzer.fit_all_factors(
        factors_name=FACTORS_NAME,
        dataset=dataset,
        per_device_batch_size=args.batch_size,
        dataloader_kwargs=loader,
        factor_args=factor_arguments(
            covariance_module_partitions=args.covariance_module_partitions,
            lambda_module_partitions=args.lambda_module_partitions,
        ),
        overwrite_output_dir=args.overwrite,
    )


def score_documents(args: argparse.Namespace) -> None:
    train_dataset = TokenWindowDataset(
        args.tokens, expected_rows=EXPECTED_RANKING_WINDOWS
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_COMMIT)
    query_dataset = ConditionalQueryDataset(args.queries, tokenizer)
    analyzer, _ = make_analyzer(
        output_dir=args.output_dir,
        gradient_checkpointing=not args.no_gradient_checkpointing,
    )
    loader = dataloader_kwargs(args.workers)
    analyzer.compute_pairwise_scores(
        scores_name=SCORES_NAME,
        factors_name=FACTORS_NAME,
        query_dataset=query_dataset,
        train_dataset=train_dataset,
        per_device_query_batch_size=args.query_batch_size,
        per_device_train_batch_size=args.train_batch_size,
        dataloader_kwargs=loader,
        score_args=score_arguments(
            query_count=EXPECTED_QUERIES,
            data_partitions=args.data_partitions,
            module_partitions=args.module_partitions,
        ),
        overwrite_output_dir=args.overwrite,
    )


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    torch.manual_seed(0)
    verify_kronfluence_version()
    print(
        f"stage={args.stage} model={MODEL_ID} commit={MODEL_COMMIT} "
        f"analysis={ANALYSIS_NAME}"
    )
    if args.stage == "fit-factors":
        fit_factors(args)
    else:
        score_documents(args)


if __name__ == "__main__":
    main()
