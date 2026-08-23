# MCP tool migration

The server accepts the v2 wire schema. Journals can contain either documented representation.

| Logical action | Journal schema | Persisted call | Current v2 wire call |
| --- | ---: | --- | --- |
| allocate | 1 | `reserve_worker(pool, count)` | `allocate_workers(pool_id, quantity, priority="normal")` |
| configure | 1 | `set_worker(worker, image)` | `configure_worker(worker_id, image_ref)` |
| publish | 1 | `publish_worker(worker)` | `publish_worker(worker_id)` |
| any | 2 | current v2 name and arguments | unchanged |

Migration changes only the wire representation. It must not change operation identity, dependencies, or logical meaning.

