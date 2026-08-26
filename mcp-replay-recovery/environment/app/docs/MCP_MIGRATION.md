# MCP tool migration

The server accepts the v2 wire schema. Journals can contain either documented representation.

| Logical action | Journal schema | Persisted call | Current v2 wire call |
| --- | ---: | --- | --- |
| allocate | 1 | `reserve_worker(pool, count)` | `allocate_workers(pool_id, quantity, priority="normal")` |
| configure | 1 | `set_worker(worker, image)` | `configure_worker(worker_id, image_ref)` |
| publish | 1 | `publish_worker(worker)` | `publish_worker(worker_id)` |
| any | 2 | current v2 name and arguments | unchanged |

Migration changes only the wire representation. It must not change operation identity, dependencies, or logical meaning.

The translated wire request becomes immutable once an attempt begins. Before the first side effect, current writers persist the exact resolved `wire_name` and `wire_arguments` beside their fingerprint in `DISPATCHED`, repeat that snapshot on current `REMOTE_OBSERVED` records, and retain it in checkpoints. Recovery of an attempted operation uses the durable snapshot verbatim even if this migration table later changes. Older attempted records without a snapshot remain compatible only while their retained fingerprint can still be reproduced from the current mapping; the next current lifecycle record upgrades them with the snapshot before another side effect.

The control tools `lookup_call`, `acquire_call`, `read_result`, and `release_result` are protocol operations, not migrated business calls. `read_result` and `release_result` both take the immutable `result_ref` and `result_sha256` receipt pair.
