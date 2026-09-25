# Proof matrix — AutonomousMemoryFormation

Checked 2026-09-25. `genvm-lint check` passed; `pytest tests/direct -q` passed 7/7. Direct mode runs the leader path with mocked source documents and LLM output; it does **not** establish live validator agreement. StudioNet RPC was unreachable during this recheck.

| Invariant or outcome | Direct test | Live evidence | Status |
| --- | --- | --- | --- |
| Pinned source deploys and exposes schema | Lint/SDK validation | [Deployment](https://explorer-studio.genlayer.com/tx/0x63923c3e8aea26ddadf5c27ebcdc25b9a29d1fdc64a7a9f7d413ee98ed022ace), [contract](https://explorer-studio.genlayer.com/address/0x1A4da26Fe77739670F8012260633F18d02796614) | Schema previously read |
| Ingest binds full-response hash and exact quote | Setup in seven tests; `test_wrong_hash_rejected_at_ingest` | [IANA ingest](https://explorer-studio.genlayer.com/tx/0x70a497d1afe4cce19aca26a072f9bcbf3e45dd276f0ed4d18b268622aba986ec) | ACTIVE fragment previously read; RFC fragment also read ACTIVE but its tx hash was not retained |
| Compaction binds two ordered ACTIVE fragments to parent epoch | `test_preserved_compaction_archives_sources`, `test_stale_proposal_cannot_consume_archived_memory` | [Proposal](https://explorer-studio.genlayer.com/tx/0x5e6f41bf7da30ad3075616ee016b3847922b755bcf729d4906432da44cc4f2b5) | Write returned ACCEPTED; final state not rechecked |
| Preserved meaning, no invented claim, and order produce capsule/archival | `test_preserved_compaction_archives_sources` | None | **Local only; live resolution unverified** |
| Loss, invented claim, or unknown result cannot archive | `test_lossy_summary_fails_closed`, `test_novel_claim_fails_closed`, `test_unknown_does_not_archive` | None | Local only |
| Unauthorized or replayed operation rejected | `test_unauthorized_and_replay_rejected` | None | Local only |
| Stale competing proposal cannot consume already archived fragments | `test_stale_proposal_cannot_consume_archived_memory` | None | Local only |

The first live `resolve_compaction` call lost RPC connectivity while polling. Its transaction ID and outcome are unknown. Do not claim a completed or finalized compaction until the receipt, `get_compaction`, both source fragment states, and `get_capsule` agree. See `LIVE_PROOFS.md` for the exact observed state.
