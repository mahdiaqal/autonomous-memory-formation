# Proof matrix — AutonomousMemoryFormation

Checked 2026-09-25. `genvm-lint check` passed; `pytest tests/direct -q` passed 7/7. Direct mode runs the leader path with mocked source documents and LLM output; it does **not** establish live validator agreement. The live StudioNet resolutions below were checked separately by receipts and contract reads.

| Invariant or outcome | Direct test | Live evidence | Status |
| --- | --- | --- | --- |
| Pinned source deploys and exposes schema | Lint/SDK validation | [Deployment](https://explorer-studio.genlayer.com/tx/0x63923c3e8aea26ddadf5c27ebcdc25b9a29d1fdc64a7a9f7d413ee98ed022ace), [contract](https://explorer-studio.genlayer.com/address/0x1A4da26Fe77739670F8012260633F18d02796614) | FINALIZED; onchain source matches local/GitHub source after newline normalization |
| Ingest binds full-response hash and exact quote | Setup in seven tests; `test_wrong_hash_rejected_at_ingest` | [RFC ingest](https://explorer-studio.genlayer.com/tx/0x3431135178da3a63b0a344bfc2bb1726e8cc476950e44f0bac8f4ee68f1ccb32), [IANA ingest](https://explorer-studio.genlayer.com/tx/0x70a497d1afe4cce19aca26a072f9bcbf3e45dd276f0ed4d18b268622aba986ec) | Both FINALIZED; matching hashes/quotes and ordered active fragments observed |
| Compaction binds two ordered ACTIVE fragments to parent epoch | `test_preserved_compaction_archives_sources`, `test_stale_proposal_cannot_consume_archived_memory` | [Proposal](https://explorer-studio.genlayer.com/tx/0x5e6f41bf7da30ad3075616ee016b3847922b755bcf729d4906432da44cc4f2b5) | FINALIZED; parent epoch 0 |
| Preserved meaning, no invented claim, and order produce capsule/archival | `test_preserved_compaction_archives_sources` | [Resolution](https://explorer-studio.genlayer.com/tx/0xd14dbe8e03a00401ebba363b6e34ed629dff21c02c2ec4684e8d821b539be3e9) | FINALIZED, MAJORITY_AGREE; `COMPACTED`, capsule active, both sources ARCHIVED, epoch 1 |
| Loss or invented claim cannot archive | `test_lossy_summary_fails_closed`, `test_novel_claim_fails_closed` | [Lossy proposal](https://explorer-studio.genlayer.com/tx/0x71c17c09d707c821fa9738d53fe6c72ebd89a80a44620182812b1f6b446ef6af), [resolution](https://explorer-studio.genlayer.com/tx/0xb865c4778e9e44a237a438765ebb6c0a347a77901689ccb884b2f57d8b78cb5b) | FINALIZED; `REJECTED`, `LOST/LOST`, novel `PRESENT`; epoch unchanged, sources ACTIVE |
| Unknown report cannot archive | `test_unknown_does_not_archive` | None | Local only |
| Unauthorized or replayed operation rejected | `test_unauthorized_and_replay_rejected` | None | Local only |
| Stale competing proposal cannot consume already archived fragments | `test_stale_proposal_cannot_consume_archived_memory` | None | Local only |

The first live `resolve_compaction` call lost RPC connectivity while polling; its hash was later recovered and its receipt and resulting state verified. See `LIVE_PROOFS.md` for the exact observed reports. Do not describe majority agreement as validator unanimity.
