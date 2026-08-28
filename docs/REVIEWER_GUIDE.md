# Reviewer guide

## What this repository contains

`mcp-replay-recovery` is an original Terminal-Bench 3 task about repairing crash-safe, schema-aware replay of MCP-style tool calls. The candidate sees a compact Python gateway and protocol documentation; the reference repair and stateful verifier are isolated from the candidate environment.

## Start here

- [Task overview](../mcp-replay-recovery/README.md)
- [Candidate instruction](../mcp-replay-recovery/instruction.md)
- [Recovery protocol](../mcp-replay-recovery/environment/app/docs/RECOVERY_PROTOCOL.md)
- [Evaluation evidence](EVALUATION.md)

## Reproduce the deterministic gates

Run these commands from the repository root with Docker available:

```bash
harbor run -p mcp-replay-recovery --agent oracle --env docker --yes
harbor run -p mcp-replay-recovery --agent nop --env docker --yes
```

The recorded 108-case checkpoint yields Oracle reward `1.000` and Nop reward `0.000`, each with zero exceptions. The task uses a separate verifier container; it receives only the declared candidate artifacts.

## Evaluation ledger

Codex calibration is complete: three independent required-configuration trials failed semantically with zero exceptions. Claude Opus 5/max calibration has one clean, documented semantic failure and two remaining trials pending available capacity. Raw Harbor artifacts are deliberately ignored because they are large, machine-specific, and may contain local execution metadata; the public result summaries, exact configurations, and failure analysis are recorded in [EVALUATION.md](EVALUATION.md).

## Design boundaries

The task's difficulty comes from real recovery invariants rather than hidden hooks or arbitrary puzzles. The verifier does not require a particular internal implementation: it checks durable state, safe external effects, recovery convergence, and documented compatibility behavior. Corrections made during calibration are recorded explicitly in the evaluation ledger; invalidated runs are not counted as frontier evidence.
