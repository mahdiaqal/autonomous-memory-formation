# StudioNet proof record

Contract: [0x1A4da26Fe77739670F8012260633F18d02796614](https://explorer-studio.genlayer.com/address/0x1A4da26Fe77739670F8012260633F18d02796614)

| Step | Transaction | Checked result |
| --- | --- | --- |
| Deploy | [0x63923c3e8aea26ddadf5c27ebcdc25b9a29d1fdc64a7a9f7d413ee98ed022ace](https://explorer-studio.genlayer.com/tx/0x63923c3e8aea26ddadf5c27ebcdc25b9a29d1fdc64a7a9f7d413ee98ed022ace) | Contract schema readable on StudioNet. |
| Ingest IANA fragment | [0x70a497d1afe4cce19aca26a072f9bcbf3e45dd276f0ed4d18b268622aba986ec](https://explorer-studio.genlayer.com/tx/0x70a497d1afe4cce19aca26a072f9bcbf3e45dd276f0ed4d18b268622aba986ec) | `get_fragment("iana-fragment")` returned ACTIVE, sequence 2, and the expected content hash. |
| Propose compaction | [0x5e6f41bf7da30ad3075616ee016b3847922b755bcf729d4906432da44cc4f2b5](https://explorer-studio.genlayer.com/tx/0x5e6f41bf7da30ad3075616ee016b3847922b755bcf729d4906432da44cc4f2b5) | Write returned ACCEPTED; terminal state not yet independently checked. |

The RFC fragment was also ingested and `get_fragment("rfc-fragment")` returned ACTIVE, sequence 1, matching hash `b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0`. Its transaction ID was not retained; do not cite a guessed link.

The first `resolve_compaction` call lost RPC connectivity while polling. Its transaction hash and final state have **not** been verified. Do not claim a successful compaction or finalized transaction until `get_compaction`, `get_capsule`, and the receipt are checked. A separate attempted IANA ingestion used an incorrect hash and did not create the fragment; it is not presented as proof.
