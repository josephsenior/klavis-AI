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
