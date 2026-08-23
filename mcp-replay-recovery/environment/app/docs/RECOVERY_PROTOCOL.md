# Recovery protocol

Each JSONL record is durable only after its complete newline has reached storage. A final byte sequence that is not a complete JSON record is a torn tail: recovery must preserve and process every valid record before it. Malformed data before the final non-empty record is corruption and must be rejected.

An operation is introduced by `PLANNED`, followed by zero or more recovery attempts. `DISPATCHED` means a request may or may not have reached the tool server. `RESULT_DURABLE` means the returned result is safely journaled. `ACKED` means local delivery is complete.

The pair `(session_id, operation_id)` is the identity of the logical operation for its entire lifetime. Attempts, schema versions, process starts, and wire-tool names are not part of that identity. A journal may multiplex multiple sessions, and operation IDs are unique only within a session. Dependencies name operations in the same session.

Every newly written lifecycle record carries both `session_id` and `operation_id`; `PLANNED` also retains the complete nested operation. Recovery remains compatible with legacy lifecycle records that omit `session_id` when their operation ID identifies exactly one planned operation in that journal. Ambiguous legacy records are corruption. The server deduplicates calls carrying a stable, collision-free encoding of the logical identity, so an uncertain dispatch remains safely retryable even when either identity component contains punctuation.

Recovery must complete a `RESULT_DURABLE` operation locally without another remote call. Other incomplete valid operations are retried when all declared dependencies have reached a durable successful result. Cyclic, missing, or failed dependencies are invalid input rather than permission to reorder calls.
