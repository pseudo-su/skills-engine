# Open questions

## Skill static analysis

Think through what static analysis would help maintain this collection before adding tooling. Consider linting, skill-format verification, references and dependencies, composition consistency, and conflicting instructions. Distinguish harness requirements from our own conventions, and investigate existing tools before writing a custom validator. Avoid treating structural checks as evidence that a skill works.

## Skill evaluations

Decide what evaluations should look like and what evidence would demonstrate improvement. Consider real execution records, fresh-session trials, representative tasks, and whether any automation is useful. Clarify what to measure, where evidence belongs, and how to avoid leaking expected answers into evaluations.

The removed evals/first-use.md was a manually authored list of suggested trial tasks and things to inspect, not an automated evaluation suite or evidence of successful runs. Its format and cases were not agreed. Keep the principle of learning from fresh use; establish the evaluation approach together before adding an evals structure.
