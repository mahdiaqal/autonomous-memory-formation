import hashlib
import json


FIRST = "The documentation reserves example.com for illustrative examples."
SECOND = "The documentation reserves example.org for illustrative examples."
SUMMARY = "First, example.com is reserved for examples; later, example.org is reserved for examples."


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def setup(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    contract = direct_deploy("contracts/AutonomousMemoryFormation.py", "public-memory")
    direct_vm.mock_web(r".*a\.example/one", {"status": 200, "body": FIRST})
    direct_vm.mock_web(r".*b\.example/two", {"status": 200, "body": SECOND})
    contract.ingest("first", "https://a.example/one", digest(FIRST), FIRST)
    contract.ingest("second", "https://b.example/two", digest(SECOND), SECOND)
    return contract


def verdict(direct_vm, coverage, novel="NONE", chronology="PRESERVED"):
    direct_vm.mock_llm(r".*Evaluate only.*", json.dumps(
        {"coverage": coverage, "novel": novel, "chronology": chronology}))


def test_preserved_compaction_archives_sources(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, ["PRESERVED", "PRESERVED"])
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    contract.resolve_compaction("c1")
    assert contract.get_compaction("c1")["state"] == "COMPACTED"
    assert contract.get_fragment("first")["state"] == "ARCHIVED"
    assert contract.get_fragment("second")["capsule_id"] == "c1"
    assert contract.get_capsule("c1")["active"] is True
    assert contract.get_state()["epoch"] == 1
    with direct_vm.expect_revert("terminal operation"):
        contract.resolve_compaction("c1")


def test_lossy_summary_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, ["PRESERVED", "LOST"])
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    contract.resolve_compaction("c1")
    assert contract.get_compaction("c1")["state"] == "REJECTED"
    assert contract.get_fragment("first")["state"] == "ACTIVE"
    assert contract.get_state()["epoch"] == 0


def test_novel_claim_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, ["PRESERVED", "PRESERVED"], novel="PRESENT")
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    contract.resolve_compaction("c1")
    assert contract.get_compaction("c1")["state"] == "REJECTED"


def test_unknown_does_not_archive(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, ["PRESERVED", "UNKNOWN"])
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    contract.resolve_compaction("c1")
    assert contract.get_compaction("c1")["state"] == "INCONCLUSIVE"
    assert contract.get_fragment("second")["state"] == "ACTIVE"


def test_wrong_hash_rejected_at_ingest(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    contract = direct_deploy("contracts/AutonomousMemoryFormation.py", "public-memory")
    direct_vm.mock_web(r".*a\.example/one", {"status": 200, "body": FIRST})
    with direct_vm.expect_revert("unavailable or mismatched"):
        contract.ingest("first", "https://a.example/one", "0" * 64, FIRST)
    assert contract.get_state()["fragment_count"] == 0


def test_unauthorized_and_replay_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("registered agent required"):
        contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    direct_vm.sender = direct_alice
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    with direct_vm.expect_revert("invalid or duplicate operation"):
        contract.propose_compaction("c1", "first", "second", SUMMARY, 0)


def test_stale_proposal_cannot_consume_archived_memory(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, ["PRESERVED", "PRESERVED"])
    contract.propose_compaction("c1", "first", "second", SUMMARY, 0)
    contract.propose_compaction("c2", "first", "second", SUMMARY, 0)
    contract.resolve_compaction("c1")
    contract.resolve_compaction("c2")
    assert contract.get_compaction("c2")["state"] == "STALE"
    assert contract.get_state()["capsule_count"] == 1
