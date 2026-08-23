# Evaluation record

## 2026-08-23 — first strengthened checkpoint

Environment:

- Harbor `0.22.0`
- Docker Desktop `4.48.0`
- Docker Engine `28.5.1`, Linux containers
- Separate verifier mode with only `/app/cli.py` and `/app/gateway` transferred

Local semantic suite:

| Candidate | Result |
| --- | --- |
| Untouched baseline | 0/15 passing |
| Reference repair | 15/15 passing |

Direct container-boundary simulation:

| Candidate | Reward |
| --- | ---: |
| Untouched baseline | 0 |
| Reference repair | 1 |

Official Harbor runs:

```bash
uvx harbor run -p mcp-replay-recovery --agent oracle --env docker --yes
uvx harbor run -p mcp-replay-recovery --agent nop --env docker --yes
```

| Agent | Trials | Exceptions | Mean reward |
| --- | ---: | ---: | ---: |
| Oracle | 1 | 0 | 1.000 |
| Nop | 1 | 0 | 0.000 |

These are development sanity runs, not the final assignment trial matrix. Rubric review, repeated Oracle reliability runs, frontier-agent calibration, failure analysis, and adversarial `/cheat` trials remain outstanding.

### Strengthened checkpoint rerun

After removing a verifier-side file-ownership artifact and applying the current Terminal-Bench metadata requirements:

| Check | Result |
| --- | --- |
| Official `checks/check-*.sh` suite | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

The Nop result therefore remains a semantic failure after the pre-seeded journal is made writable by the unprivileged candidate process.

### First Codex pilot

Configuration:

```bash
uvx harbor run -p mcp-replay-recovery --agent codex --model openai/gpt-5.6-sol --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh
```

| Trials | Exceptions | Reward | Runtime |
| ---: | ---: | ---: | ---: |
| 1 | 0 | 1.000 | 17m 14s |

Codex identified the four direct defect classes and produced a repair close to the Oracle. This established that the 15-test checkpoint was under-calibrated for the required frontier configuration.

### Multiplexed-journal checkpoint

Two professional identity cases were added: multiple sessions with repeated operation IDs in one journal, and identity components whose naive delimiter concatenation collides. New lifecycle events are session-qualified while legacy records remain valid when unambiguous.

| Check | Result |
| --- | --- |
| Local reference repair | 17/17 pass |
| Local untouched baseline | 0/17 pass |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

### Second Codex pilot — invalidated

The multiplexed-journal pilot completed with 0 exceptions and an apparent reward of 0.000. Inspection showed 16/17 tests passed; the only failure required all independent allocations across sessions to occur before any configuration. That global layer ordering was not required by the task or recovery protocol. The candidate's interleaving respected every declared dependency, so the verifier assertion was corrected and this run is excluded from calibration evidence.

The run also encountered an agent setup timeout on its first attempt and an editor/model-manager delay on the valid attempt. Those infrastructure events did not determine the hidden-test failure, but are recorded for reproducibility.

### Durable result-binding checkpoint

Operations may now recursively bind arguments to fields in durable results of same-session transitive dependencies. The verifier exercises opaque server-generated identifiers, multiplexed sessions with reused operation IDs, v1-to-v2 migration, and a crash immediately after the producer result becomes durable.

| Check | Result |
| --- | --- |
| Local reference repair | 19/19 pass |
| Local untouched baseline | 0/19 pass |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

### Result-binding Codex pilot

The valid 19-test checkpoint was run with the required Codex model and reasoning configuration plus a 3× agent-setup timeout multiplier to tolerate dependency installation. The task execution budget was unchanged.

| Trials | Exceptions | Reward | Runtime |
| ---: | ---: | ---: | ---: |
| 1 | 0 | 1.000 | 19m 30s |

Codex implemented composite identity, durable result reconstruction, recursive path binding, transitive dependency validation, legacy compatibility, schema migration, and journal-tail repair. This checkpoint remains under-calibrated for final submission despite being substantially stronger and more realistic than the initial version.
