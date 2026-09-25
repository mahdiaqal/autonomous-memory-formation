# AutonomousMemoryFormation

Consensus-gated compaction for shared agent memory. This is not a truth oracle, knowledge graph, certificate, reputation system, or private-memory store.

## Problem

Agent memory grows without a safe way to replace redundant fragments. An ordinary database can store and link fragments, but a multi-agent system needs independent agreement before an irreversible compaction discards its active source view.

## Consensus boundary

An agent registers a public HTTPS document and an exact quote. The contract fetches the document and requires its SHA-256 hash and quote to match before assigning the next sequence number. A registered agent may propose a bounded summary of two ordered fragments. During resolution, GenLayer leader and validators **independently re-fetch both full documents**, recompute their hashes, check both quotes, and compare the summary against those source texts. The complete report must match exactly. The contract never treats a URL, hash length, nonempty summary, or agent assertion as proof that meaning was preserved.

Only a report with `PRESERVED/PRESERVED`, no novel material claim, and preserved chronological order produces a capsule and archives the two source fragments. `LOST`, `PRESENT`, or broken order rejects the proposal. Missing, stale, mismatched, or uncertain observations fail closed. Original URLs, quotes, hashes, and an append-only operation record remain retrievable after compaction. No claim is made that the documents themselves are true.

## Lifecycle

`ingest` → `ACTIVE` fragments → `propose_compaction` → independent re-fetch and validator comparison → `COMPACTED` capsule with `ARCHIVED` sources, or `REJECTED` / `INCONCLUSIVE` / `STALE` without archival.

The operation ID is unique, a proposal binds its parent epoch and ordered fragment IDs, and terminal operations cannot be replayed. The capsule is a retrieval optimization, not a one-time consumable certificate. A new compaction cannot reuse archived fragments.

## API

`register_agent`, `ingest`, `propose_compaction`, `resolve_compaction`, `get_state`, `get_fragment`, `get_compaction`, `get_capsule`, `get_record`.

## Limits and threat model

Public text only; never submit private user data. Two fragments per compaction, quotes 16–500 characters, summary 20–800 characters, fetched document 16 KiB maximum. The contract rejects non-HTTPS URLs and obvious local hostnames, but deployers should also restrict outbound egress at the GenVM/network layer against DNS rebinding. Source edits are detected by hash. Prompt injection in fetched documents is treated as untrusted text; exact validator agreement and fail-closed outcomes are additional safeguards, not guarantees of semantic correctness. A consensus-valid decision reflects the validators' interpretation of the fixed source bytes, not external truth.

## Run

```powershell
genvm-lint check contracts/AutonomousMemoryFormation.py
pytest tests/direct/ -v
genlayer network set studionet
genlayer deploy --contract contracts/AutonomousMemoryFormation.py --args public-memory
genlayer schema <address>
```

See `LIVE_PROOFS.md` for transaction evidence after deployment. Do not represent an unfinalized or reverted transaction as a successful memory transition.
