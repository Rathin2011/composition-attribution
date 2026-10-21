"""Task definitions shared by the generalized composition experiments.

This module is deliberately limited to task semantics.  It does not load a
model, calculate lens values, run interventions, or write result files.

All Khandelwal--Pavlick tasks are represented in the same canonical form:

``x``
    The query value, such as a landmark.
``Fx``
    The intermediate value, such as a country.
``GFx``
    The composed answer, such as a capital.

Later experiment stages can therefore operate on :class:`TaskExample` objects
without containing task-specific conditionals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


DATASET_ID = "apoorvkh/composing-functions"
DATASET_COMMIT = "5b7b70743ff849eae3875dc0c22d5443066b33e9"


@dataclass(frozen=True)
class TaskExample:
    """One canonical ``x -> Fx -> GFx`` dataset row."""

    x: str
    Fx: str
    GFx: str

    @classmethod
    def from_dataset_row(cls, row: Mapping[str, Any]) -> "TaskExample":
        """Validate and convert one Hugging Face dataset row.

        Input:
            A mapping containing the string fields ``x``, ``Fx``, and ``GFx``.
        Output:
            An immutable :class:`TaskExample`.
        """

        values = {}
        for field in ("x", "Fx", "GFx"):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"dataset field {field!r} must be a non-empty string")
            values[field] = value
        return cls(**values)

    def overlaps(self, other: "TaskExample") -> bool:
        """Return whether two rows share any ``x``, ``Fx``, or ``GFx`` value."""

        return bool(
            {self.x, self.Fx, self.GFx}
            & {other.x, other.Fx, other.GFx}
        )

    def as_dict(self) -> dict[str, str]:
        """Return the canonical JSON representation used by every stage."""

        return {"x": self.x, "Fx": self.Fx, "GFx": self.GFx}


@dataclass(frozen=True)
class TaskSpec:
    """Everything the shared pipeline needs to know about one task.

    ``dataset_task`` selects rows from the paper dataset.  The three ``*_name``
    fields are human-readable labels only; stored records always retain the
    canonical keys ``x``, ``Fx``, and ``GFx``.
    """

    dataset_task: str
    x_name: str
    fx_name: str
    gfx_name: str
    expected_rows: int | None = None
    numeric_nodes: tuple[str, ...] = ()

    def target_text(self, node: str, value: str) -> str:
        """Text to tokenize/compare for this node, following the paper's spacing.

        Numeric nodes omit the leading space so their first token is numeric.
        Word nodes retain it because tokenizers commonly merge space + word.
        """
        if node not in ("x", "Fx", "GFx"):
            raise ValueError(f"unknown task node: {node!r}")
        return value if node in self.numeric_nodes else f" {value}"

    def token_ids(self, tokenizer: Any, node: str, value: str) -> list[int]:
        """Encode a complete value; reject whitespace as a numeric target."""
        ids = [int(t) for t in tokenizer.encode(
            self.target_text(node, value), add_special_tokens=False
        )]
        if not ids:
            raise ValueError(f"task value has no tokens: {value!r}")
        if node in self.numeric_nodes and not tokenizer.decode([ids[0]]).strip():
            raise ValueError(f"numeric {node} starts with a whitespace token: {value!r}")
        return ids

    @property
    def answer_prefix(self) -> str:
        return "A: " if "GFx" in self.numeric_nodes else "A:"

    @property
    def target_definition(self) -> str:
        return "task_aware_first_token" if self.numeric_nodes else "leading_space_first_token"

    def validate_prompt(self, prompt: str, x: str) -> None:
        """Reject stale manifests with an incompatible answer prefix."""
        suffix = f"Q: {x}\n{self.answer_prefix}"
        if not prompt.endswith(suffix):
            raise ValueError(
                f"prompt must end with {suffix!r}; regenerate the task manifest"
            )

    def select_examples(
        self, rows: Iterable[Mapping[str, Any]]
    ) -> list[TaskExample]:
        """Select this task's rows and convert them to canonical examples.

        Input:
            Rows from the pinned Khandelwal--Pavlick dataset.
        Output:
            Ordered examples whose ``task`` field equals ``dataset_task``.
        """

        examples = [
            TaskExample.from_dataset_row(row)
            for row in rows
            if row.get("task") == self.dataset_task
        ]
        if self.expected_rows is not None and len(examples) != self.expected_rows:
            raise ValueError(
                f"expected {self.expected_rows} rows for {self.dataset_task!r}, "
                f"found {len(examples)}"
            )
        return examples

    def render_prompt(
        self, context: Iterable[TaskExample], query: TaskExample
    ) -> str:
        """Render the paper's composition prompt for this task.

        Demonstrations expose ``x -> GFx``.  The final answer is omitted so the
        causal language model must predict ``query.GFx``.
        """

        demonstrations = "".join(
            f"Q: {example.x}\nA: {example.GFx}\n\n" for example in context
        )
        return f"{demonstrations}Q: {query.x}\n{self.answer_prefix}"

    def validate_intervention_target(
        self, query: TaskExample, target: TaskExample
    ) -> None:
        """Reject an intervention target that is not counterfactual.

        The target row supplies both the alternative ``Fx`` direction and its
        corresponding ``GFx`` output.  They must both differ from the query.
        """

        if target.Fx == query.Fx:
            raise ValueError("intervention target must have a different Fx")
        if target.GFx == query.GFx:
            raise ValueError("intervention target must have a different GFx")


LANDMARK_COUNTRY_CAPITAL = TaskSpec(
    dataset_task="landmark-country-capital",
    x_name="landmark",
    fx_name="country",
    gfx_name="capital",
    expected_rows=1_385,
)


def _task(
    dataset_task: str,
    x_name: str,
    fx_name: str,
    gfx_name: str,
    expected_rows: int,
) -> TaskSpec:
    """Construct a registered task specification concisely."""

    numeric_nodes = {
        "book-author-birthyear": ("GFx",),
        "movie-director-birthyear": ("GFx",),
        "song-artist-birthyear": ("GFx",),
        "person-university-year": ("GFx",),
        "mod-twenty-times-two": ("x", "Fx", "GFx"),
        "plus-hundred-times-two": ("x", "Fx", "GFx"),
        "plus-ten-times-two": ("x", "Fx", "GFx"),
        "word-int-times-two": ("Fx", "GFx"),
    }.get(dataset_task, ())
    return TaskSpec(dataset_task, x_name, fx_name, gfx_name, expected_rows, numeric_nodes)


# Row counts were checked against the pinned dataset commit above.  Human-readable
# node names document task semantics; every saved record still uses x/Fx/GFx.
TASKS: dict[str, TaskSpec] = {
    task.dataset_task: task
    for task in (
        _task("antonym-french", "word", "antonym", "French translation", 2_398),
        _task("antonym-german", "word", "antonym", "German translation", 2_398),
        _task("antonym-spanish", "word", "antonym", "Spanish translation", 2_398),
        _task("book-author-birthyear", "book", "author", "birth year", 2_228),
        LANDMARK_COUNTRY_CAPITAL,
        _task("mod-twenty-times-two", "integer", "modulo 20", "times two", 1_000),
        _task("movie-director-birthyear", "movie", "director", "birth year", 2_180),
        _task("park-country-capital", "park", "country", "capital", 743),
        _task("person-university-founder", "person", "university", "founder", 4_996),
        _task("person-university-year", "person", "university", "founding year", 4_992),
        _task("plus-hundred-times-two", "integer", "plus 100", "times two", 1_000),
        _task("plus-ten-times-two", "integer", "plus 10", "times two", 1_000),
        _task("product-company-ceo", "product", "company", "CEO", 1_904),
        _task("product-company-hq", "product", "company", "headquarters", 2_276),
        _task("rgb-rot120-name", "RGB value", "rotated RGB", "color name", 1_000),
        _task("song-artist-birthyear", "song", "artist", "birth year", 958),
        _task("word-int-times-two", "number word", "integer", "times two", 1_000),
        _task("word-substring-reverse", "word", "substring", "reversed substring", 2_946),
    )
}


def get_task_spec(name: str) -> TaskSpec:
    """Return a registered task or raise an error listing valid names."""

    try:
        return TASKS[name]
    except KeyError as error:
        choices = ", ".join(sorted(TASKS))
        raise ValueError(f"unknown task {name!r}; available tasks: {choices}") from error
