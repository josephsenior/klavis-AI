# Recovery protocol

Each JSONL record is durable only after its complete newline has reached storage. A final byte sequence that is not a complete JSON record is a torn tail: recovery must preserve and process every valid record before it, truncate the incomplete bytes while holding journal ownership, and only then append new lifecycle records. Malformed data before the final non-empty record is corruption and must be rejected.

An operation is introduced by `PLANNED`, followed by zero or more recovery attempts. `DISPATCHED` means a request may or may not have reached the tool server. `RESULT_DURABLE` means the returned result is safely journaled. `ACKED` means local delivery is complete.

The pair `(session_id, operation_id)` is the identity of the logical operation for its entire lifetime. Attempts, schema versions, process starts, and wire-tool names are not part of that identity. A journal may multiplex multiple sessions, and operation IDs are unique only within a session. Dependencies name operations in the same session.

Every newly written lifecycle record carries both `session_id` and `operation_id`; `PLANNED` also retains the complete nested operation. Recovery remains compatible with legacy lifecycle records that omit `session_id` when their operation ID identifies exactly one planned operation in that journal. Ambiguous legacy records are corruption. The server deduplicates calls carrying a stable, collision-free encoding of the logical identity, so an uncertain dispatch remains safely retryable even when either identity component contains punctuation.

Recovery must complete a `RESULT_DURABLE` operation locally without another remote call. Other incomplete valid operations are retried when all declared dependencies have reached a durable successful result. Cyclic, missing, or failed dependencies are invalid input rather than permission to reorder calls.

Persisted arguments may bind values from a prior result using `{"$result":{"operation_id":"allocate","path":["worker_ids",0]}}`. Bindings can appear recursively inside argument objects or arrays. The referenced operation is scoped to the same session and must be a declared transitive dependency. `path` traverses object keys and array indexes in order. Recovery resolves bindings from the durable result recorded in the journal; it must not redispatch a completed producer merely to reconstruct its output. Invalid references are rejected rather than sent to the tool server.

Only one recovery invocation may own a journal at a time. The ownership interval begins before loading recovery state and ends after the final lifecycle record is durable. Concurrent invocations for the same journal wait for that owner, then reconstruct the new state; they must not emit duplicate `DISPATCHED`, `RESULT_DURABLE`, or `ACKED` records for work completed by the first owner. Ownership is automatically released if its process crashes so a waiter can safely retry an uncertain dispatch. Journals at different paths remain independent.

Production journals may contain thousands of operations and dependency chains deeper than the Python recursion limit. Validation and scheduling must be stack-safe and linear in the operation/dependency graph apart from the actual traversal needed for result bindings. A complete 4,096-operation chain is a supported journal, not corrupt input.
