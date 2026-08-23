# MCP replay recovery

This repository is an in-progress Terminal-Bench 3 task about repairing durable MCP tool execution across crashes and schema evolution.

The candidate receives a compact Python gateway with a functioning v2 happy path and several interacting recovery defects. The separate verifier owns the remote tool server, injects crashes at semantic boundaries, and evaluates externally visible effects rather than trusting the gateway's local state.

## Capability hypothesis

Frontier coding agents are strong at localized bug fixing but still struggle to preserve global invariants that span a persistent journal, uncertain remote outcomes, idempotency identity, schema migration, and causal dependencies. A plausible but incomplete repair often solves duplication by losing work, solves migration while changing identity, or replays successfully while violating ordering.

## Current status

| Check | Result |
| --- | --- |
| Deterministic verifier scenarios | 6 implemented |
| Nop/local baseline | 0/6 tests pass |
| Oracle/local reference repair | 6/6 tests pass |
| Separate verifier structure | Implemented |
| Docker image build | Pending Docker Desktop Linux engine |
| Harbor Oracle/Nop runs | Pending Harbor installation and Docker validation |
| Codex/Claude calibration | Not started |
| Adversarial `/cheat` trials | Not started |

The current verifier covers uncertain remote commits, crashes after durable local results, v1-to-v2 replay, dependency ordering independent of journal order, torn journal tails, and crash/restart convergence.

## Repository layout

- `mcp-replay-recovery/environment/app/`: candidate-visible gateway, protocol documentation, and example input.
- `mcp-replay-recovery/tests/`: separate verifier image, hidden stateful tool server, and deterministic scenarios.
- `mcp-replay-recovery/solution/`: production-style reference repair used by the Oracle agent.
- `mcp-replay-recovery/task.toml`: Harbor task metadata, resources, artifacts, and separate-verifier configuration.

## Planned validation

Once Docker Desktop and Harbor are available:

```bash
harbor run -p mcp-replay-recovery --agent oracle --env docker --yes
harbor run -p mcp-replay-recovery --agent nop --env docker --yes
```

After Oracle=1 and Nop=0 are repeatable in Harbor, the next stage is static/rubric review, adversarial verifier hardening, one Codex pilot, failure-guided calibration, and only then the required standard and `/cheat` trial matrix.

