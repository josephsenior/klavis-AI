# MCP replay recovery

This repository is an in-progress Terminal-Bench 3 task about repairing durable MCP tool execution across crashes and schema evolution.

The candidate receives a compact Python gateway with a functioning v2 happy path and several interacting recovery defects. The separate verifier owns the remote tool server, injects crashes at semantic boundaries, and evaluates externally visible effects rather than trusting the gateway's local state.

## Capability hypothesis

Frontier coding agents are strong at localized bug fixing but still struggle to preserve global invariants that span a persistent journal, uncertain remote outcomes, idempotency identity, schema migration, and causal dependencies. A plausible but incomplete repair often solves duplication by losing work, solves migration while changing identity, or replays successfully while violating ordering.

## Current status

| Check | Result |
| --- | --- |
| Deterministic verifier scenarios | 22 implemented, including 5 generated seeds |
| Nop/local baseline | 1/22 tests pass; overall reward 0 |
| Oracle/local reference repair | 22/22 tests pass |
| Separate verifier structure | Implemented and container-tested |
| Docker image build | Agent and verifier images build successfully |
| Harbor Oracle/Nop runs | Oracle=1.000, Nop=0.000, zero exceptions |
| Official static checks | 22/22 pass |
| Codex calibration | Two valid pilots passed; two apparent failures invalidated; corrected rerun pending |
| Claude calibration | Not started |
| Adversarial `/cheat` trials | Not started |

The current verifier covers uncertain remote commits, pre-receipt crashes, repeated uncertain restarts, crashes after durable local results, recursive result-bound arguments, mixed v1/v2 replay, dependency ordering independent of journal order, multiplexed sessions with reused operation IDs, delimiter-safe idempotency identity, torn-tail repair before later appends, concurrent recovery ownership and owner-crash failover, a 4,096-operation dependency chain, invalid dependency graphs, and crash/restart convergence.

## Repository layout

- `mcp-replay-recovery/environment/app/`: candidate-visible gateway, protocol documentation, and example input.
- `mcp-replay-recovery/tests/`: separate verifier image, hidden stateful tool server, and deterministic scenarios.
- `mcp-replay-recovery/solution/`: production-style reference repair used by the Oracle agent.
- `mcp-replay-recovery/task.toml`: Harbor task metadata, resources, artifacts, and separate-verifier configuration.

## Planned validation

Current sanity commands:

```bash
harbor run -p mcp-replay-recovery --agent oracle --env docker --yes
harbor run -p mcp-replay-recovery --agent nop --env docker --yes
```

The next stage is rubric review, adversarial verifier hardening, one Codex pilot, failure-guided calibration, and only then the required standard and `/cheat` trial matrix. See `docs/EVALUATION.md` for recorded runs.
