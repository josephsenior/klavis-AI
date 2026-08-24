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

### Concurrent scale checkpoint

The protocol now requires one process-level recovery owner per journal, automatic lease release on process death, stack-safe linear dependency validation for a documented 4,096-operation chain, and truncation of a torn tail before any new lifecycle append. The environment image also bakes the system prerequisites Harbor's Codex adapter otherwise installs at trial time.

| Check | Result |
| --- | --- |
| Local reference repair | 22/22 pass |
| Local untouched baseline | 1/22 pass; overall reward 0 |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

The untouched baseline's one passing case is the already-complete scale journal: it performs no graph validation and therefore returns without work. It still fails the benchmark as a whole.

### Concurrent scale Codex pilot — invalidated

Two attempts with 3× and 6× setup multipliers completed zero trials because Harbor stalled while installing missing OS packages. The prerequisites were then added to the environment image, after which a valid Codex trial completed with 0 exceptions and an apparent reward of 0.000 in 21m 50s.

Inspection showed 20/21 tests passed, including the overlapping-recoverer case. The only failure came from a synthetic scale fixture that recorded `PLANNED → RESULT_DURABLE → ACKED` while omitting the `DISPATCHED` event a real completed operation would contain. Codex reasonably rejected that lifecycle as corruption. The fixture now records the valid lifecycle, the apparent failure is excluded from calibration evidence, and the corrected 22-test checkpoint still requires a valid frontier rerun.

### Plan-continuation checkpoint

`execute` now repairs an existing torn tail before writing any new `PLANNED` record and holds one reentrant ownership interval through planning and recovery. The hidden continuation case combines an uncertain opaque allocation result, a torn write, a newly appended dependent operation, and result binding after replay.

| Check | Result |
| --- | --- |
| Local reference repair | 23/23 pass |
| New case against untouched baseline | fail |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

A valid Codex/xhigh pilot passed all 23 tests with 0 exceptions and reward 1.000 in 22m 26s. This demonstrated that atomic plan continuation alone did not calibrate the task above the required frontier configuration.

### Dispatch-key migration checkpoint

New dispatch records persist the exact idempotency key sent remotely. Once durable, that key is authoritative across retries even when a newer gateway version would derive a different encoding. The hidden case simulates a v1 call already committed under a historical key, then requires v2 replay to recover its opaque result and configure the dependent resource without another allocation.

| Check | Result |
| --- | --- |
| Local reference repair | 24/24 pass |
| New case against untouched baseline | fail |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

The first Codex/xhigh attempt at this checkpoint is invalid calibration evidence. The response stream disconnected shortly after initial file edits, all reconnects then failed DNS resolution for `chatgpt.com`, and Harbor eventually reported `AgentTimeoutError` at the unchanged 7,200-second task limit. The incomplete artifact passed 3/24 tests, but that result is attributed to the recorded network outage rather than model capability.

After Docker DNS resolution was independently verified, a clean replacement trial completed with 0 exceptions and reward 1.000 in 24m 56s. Codex correctly treated the persisted historical dispatch key as authoritative while also satisfying the other 23 recovery cases. The 24-test checkpoint therefore remains under-calibrated for final submission.

### Remote-reconciliation checkpoint

The verifier now distinguishes the tool server's short-lived request-deduplication cache from a durable outcome ledger. The hidden case simulates a side effect committed under a historical dispatch key, expires only its dedupe entry, and then requires recovery to reconcile the authoritative remote result before retry. The recovered opaque worker ID must also flow into a dependent configuration operation.

| Check | Result |
| --- | --- |
| Local reference repair | 25/25 pass |
| New case against untouched baseline | fail |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

A clean Codex/xhigh pilot passed all 25 tests with 0 exceptions and reward 1.000 in 28m 13s. Trajectory inspection showed that Codex implemented lookup-before-retry directly and used unique transport identities for read-only lookups to avoid stale negative-response caching. This fifth valid successful pilot confirms that the single-state remote-reconciliation checkpoint is also under-calibrated for final submission.

### Checkpoint/compaction checkpoint

The task now has a documented `compact` command and checksummed normalized checkpoint format. Compaction atomically publishes the checkpoint before truncating the exact journal prefix it covers. Recovery must merge compacted state with only the uncovered suffix, including when a crash leaves both the active checkpoint and its original covered prefix. Terminal results and uncertain dispatch keys must survive compaction so later result bindings and remote reconciliation remain correct.

| Check | Result |
| --- | --- |
| Local reference repair | 29/29 pass |
| Official static checks | 22/22 pass |
| Harbor Oracle | 1 trial, 0 exceptions, reward 1.000 |
| Harbor Nop | 1 trial, 0 exceptions, reward 0.000 |

The first Codex/xhigh attempt reported reward 0.000 with zero exceptions in 23m 35s, but its only two failures were verifier defects. One fixture required an undisclosed internal fault-hook name instead of constructing the documented post-publication crash state externally; the other required an exact error-message substring even though the candidate correctly rejected the checksum-invalid active checkpoint. That run is invalidated and excluded from calibration evidence. The verifier now restores the covered prefix directly after successful compaction and checks only nonzero rejection of corrupt active checkpoints.

A clean replacement trial against the corrected 29-test verifier passed with 0 exceptions and reward 1.000 in 28m 18s. The artifact implemented checksummed normalized state, exact covered-prefix hashing, checkpoint-plus-suffix recovery, post-compaction planning, uncertain-dispatch reconciliation, and active-checkpoint integrity. This sixth valid successful pilot shows that checkpoint/compaction substantially broadens the architecture but remains under-calibrated for the required Codex configuration.

A second clean Codex/xhigh reliability sample was run directly from pushed commit `c582312`. It passed all 29 tests with 0 exceptions and reward 1.000 in 25m 51s. Trajectory inspection again showed a coherent independent reconstruction of the recovery subsystem rather than a verifier shortcut: the candidate implemented atomic normalized checkpoints, covered-prefix handling, schema migration, scoped bindings, concurrent ownership, and uncertain-outcome reconciliation. The corrected checkpoint/compaction version is therefore 2/2 for Codex and is definitively under-calibrated relative to the required frontier-failure threshold.
