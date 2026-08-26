# MCP replay recovery

This repository is an in-progress Terminal-Bench 3 task about repairing durable MCP tool execution across crashes and schema evolution.

The candidate receives a compact Python gateway with a functioning v2 happy path and several interacting recovery defects. The separate verifier owns the remote tool server, injects crashes at semantic boundaries, and evaluates externally visible effects rather than trusting the gateway's local state.

## Capability hypothesis

Frontier coding agents are strong at localized bug fixing but still struggle to preserve global invariants that span a persistent journal, uncertain remote outcomes, idempotency identity, schema migration, and causal dependencies. A plausible but incomplete repair often solves duplication by losing work, solves migration while changing identity, or replays successfully while violating ordering.

## Current status

| Check | Result |
| --- | --- |
| Deterministic verifier scenarios | 99 pytest cases, including generated mixed-schema seeds and crash matrices |
| Nop baseline | 42/99 pass; overall reward 0 |
| Oracle reference repair | 98 pass + 1 platform skip locally; 99/99 pass in Docker |
| Separate verifier structure | Implemented and container-tested |
| Docker image build | Agent and verifier images build successfully |
| Harbor Oracle/Nop runs | Oracle=1.000, Nop=0.000, zero exceptions on the 99-case checkpoint |
| Official static checks | 22/22 pass against the current public contract |
| Codex calibration | Nine valid pilots passed through 90 tests; the corrected fresh 94-test artifact passes, while that frozen artifact fails all five new wire-snapshot cases; a fresh 99-test trial is pending |
| Claude calibration | Not started |
| Adversarial `/cheat` trials | Not started |

The current verifier covers uncertain remote commits, immutable resolved wire-request snapshots across migration-code drift, durable authoritative commit receipts, offloaded result materialization, fenced successor generations, monotonic authority revisions, crash-safe result release, cooperative polling without head-of-line blocking, atomic content-addressed checkpoint publication and compaction, checkpoint lineage and integrity, mixed v1/v2 replay, historical dispatch-key reuse, dependency ordering, multiplexed sessions, collision-free identity, torn-tail and directory-durability repair, concurrent ownership and failover, a 4,096-operation dependency chain, invalid dependency graphs, and crash/restart convergence.

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

The cooperative scheduler checkpoint was under-calibrated. The current immutable wire-snapshot refinement passes the complete local reference suite, all static and Docker gates, and has differential evidence against the frozen prior Codex artifact; fresh frontier validation is still in progress. Only genuine, contract-compliant failures will count toward the required repeated frontier and `/cheat` matrix. See `docs/EVALUATION.md` for recorded runs.
