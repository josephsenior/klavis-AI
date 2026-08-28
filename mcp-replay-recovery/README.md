# MCP replay recovery

Repair a Python gateway that executes MCP-style tool calls, persists their lifecycle, and must recover safely after crashes, schema migration, remote uncertainty, and journal compaction.

## Difficulty explanation

This task combines distributed-systems recovery, durable storage, and schema-evolution reasoning: a locally plausible repair can preserve at-most-once effects yet silently lose liveness, or replay work while violating durable identity and dependency guarantees. The difficult cases occur at boundaries—before a remote authority response is journaled, after compaction, and when a valid repeated plan extends an existing logical operation.

## Solution explanation

A correct repair treats the persisted lifecycle as the source of truth: it durably prepares the exact resolved request before authority acquisition, reconciles uncertain remote state without changing identity, and preserves valid checkpoint lineage during compaction. It also admits multi-operation plans atomically, so an incomplete durable prefix cannot become executable and an identical continuation can safely complete it.

## Verification explanation

The separate verifier drives an unprivileged candidate gateway against a stateful remote server that injects lost responses, delayed visibility, migration drift, crashes, compaction, and stale generations. It evaluates durable artifacts and externally visible remote effects, including liveness and causal ordering, rather than trusting candidate-reported status.

## Relevant experience

This task draws on experience building and evaluating long-horizon coding-agent infrastructure where durable execution, replay, verification, and failure recovery must compose under partial failure.
