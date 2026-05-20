import json
from pathlib import Path

import pytest

from workflow_agent_studio.blueprint.review import (
    ApprovalBlockedError,
    add_review_comment,
    approve_blueprint,
    diff_blueprints,
    edit_blueprint,
    record_blueprint_diff,
    record_review_feedback,
    summarize_review_feedback,
)
from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.domain.review import REVIEW_FEEDBACK_CATEGORIES, ReviewFeedback
from workflow_agent_studio.domain.workflow import EvidenceReference
from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintApprovalRepository,
    BlueprintVersionRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)


@pytest.fixture()
def connection(tmp_path):
    database = connect_database(tmp_path / "workflow_studio.sqlite3")
    initialize_database(database)
    try:
        yield database
    finally:
        database.close()


def _valid_blueprint() -> AutomationBlueprint:
    data = json.loads(
        Path("tests/fixtures/blueprints/minimal_valid.json").read_text(encoding="utf-8")
    )
    return AutomationBlueprint.model_validate(data)


def test_blueprint_edit_creates_new_version(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    versions = BlueprintVersionRepository(connection)
    audit_events = AuditEventRepository(connection)
    original = _valid_blueprint()
    edited = original.model_copy(update={"rough_effort_band": "medium"})

    first = edit_blueprint(
        run_id="run-1",
        blueprint=original,
        editor_label="operator",
        versions=versions,
        audit_events=audit_events,
    )
    second = edit_blueprint(
        run_id="run-1",
        blueprint=edited,
        editor_label="operator",
        versions=versions,
        audit_events=audit_events,
    )

    stored_versions = versions.list_versions("run-1")
    assert [version.version_number for version in stored_versions] == [1, 2]
    assert first.blueprint_version_id != second.blueprint_version_id
    assert json.loads(stored_versions[0].blueprint_json)["rough_effort_band"] == "small"
    assert json.loads(stored_versions[1].blueprint_json)["rough_effort_band"] == "medium"


def test_blocking_findings_prevent_approval(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    versions = BlueprintVersionRepository(connection)
    invalid = _valid_blueprint().model_copy(update={"eval_cases": []})
    version = versions.add_version(
        run_id="run-1",
        blueprint=invalid.model_dump(mode="json"),
    )

    with pytest.raises(ApprovalBlockedError) as error:
        approve_blueprint(
            blueprint=invalid,
            version=version,
            reviewer_label="operator",
            approvals=BlueprintApprovalRepository(connection),
            audit_events=AuditEventRepository(connection),
        )

    assert any(finding.section == "eval_cases" for finding in error.value.findings)
    assert (
        BlueprintApprovalRepository(connection).get_approval(version.blueprint_version_id) is None
    )
    assert AuditEventRepository(connection).list_events("run-1") == []


def test_approval_validates_the_stored_version_payload(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    versions = BlueprintVersionRepository(connection)
    valid = _valid_blueprint()
    invalid = valid.model_copy(update={"eval_cases": []})
    version = versions.add_version(
        run_id="run-1",
        blueprint=invalid.model_dump(mode="json"),
    )

    with pytest.raises(ApprovalBlockedError) as error:
        approve_blueprint(
            blueprint=valid,
            version=version,
            reviewer_label="operator",
            approvals=BlueprintApprovalRepository(connection),
            audit_events=AuditEventRepository(connection),
        )

    assert any(finding.rule_id == "PLAN-VERSION-MISMATCH" for finding in error.value.findings)
    assert (
        BlueprintApprovalRepository(connection).get_approval(version.blueprint_version_id) is None
    )


def test_valid_blueprint_approval_records_audit_event(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    versions = BlueprintVersionRepository(connection)
    approvals = BlueprintApprovalRepository(connection)
    audit_events = AuditEventRepository(connection)
    blueprint = _valid_blueprint()
    version = versions.add_version(
        run_id="run-1",
        blueprint=blueprint.model_dump(mode="json"),
    )

    approved = approve_blueprint(
        blueprint=blueprint,
        version=version,
        reviewer_label="operator",
        approvals=approvals,
        audit_events=audit_events,
        approved_at="2026-05-19T00:00:00+00:00",
    )

    assert approved.approval.blueprint_version_id == version.blueprint_version_id
    assert approved.approval.reviewer_label == "operator"
    assert approved.approval.approved_at == "2026-05-19T00:00:00+00:00"
    assert approved.approval.status == "approved"
    event = audit_events.list_events("run-1")[0]
    payload = json.loads(event["payload_json"])
    assert event["event_type"] == "blueprint_approved"
    assert payload["blueprint_version_id"] == version.blueprint_version_id
    assert payload["reviewer_label"] == "operator"


def test_review_comment_attaches_to_section_and_evidence_without_auditing_text(
    connection,
) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    audit_events = AuditEventRepository(connection)
    comment = add_review_comment(
        run_id="run-1",
        blueprint_version_id=1,
        section="workflow_summary",
        reviewer_label="operator",
        comment_text="Raw confidential source text should not be audited.",
        evidence_reference=EvidenceReference(source_id="src-1", chunk_id="chk-1"),
        audit_events=audit_events,
        commented_at="2026-05-20T00:00:00+00:00",
    )

    assert comment.section == "workflow_summary"
    assert comment.evidence_reference == EvidenceReference(source_id="src-1", chunk_id="chk-1")

    event = audit_events.list_events("run-1")[0]
    payload = json.loads(event["payload_json"])
    assert event["event_type"] == "review_comment_added"
    assert payload["section"] == "workflow_summary"
    assert payload["evidence_reference"] == {"chunk_id": "chk-1", "source_id": "src-1"}
    assert "Raw confidential source text" not in event["payload_json"]


def test_blueprint_diff_tracks_review_relevant_sections_without_auditing_claim_text(
    connection,
) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    audit_events = AuditEventRepository(connection)
    previous = _valid_blueprint()
    current = previous.model_copy(
        update={
            "workflow_summary": previous.workflow_summary.model_copy(
                update={"text": "Changed confidential claim text."}
            ),
            "human_approval_boundaries": [],
        }
    )

    diff = diff_blueprints(
        previous=previous,
        current=current,
        previous_version_id=1,
        current_version_id=2,
    )
    record_blueprint_diff(run_id="run-1", diff=diff, audit_events=audit_events)

    assert {entry.section for entry in diff.entries} == {
        "workflow_summary",
        "findings",
        "approval_boundaries",
    }
    event = audit_events.list_events("run-1")[0]
    payload = json.loads(event["payload_json"])
    assert event["event_type"] == "blueprint_diff_recorded"
    assert payload["changed_sections"] == [
        "workflow_summary",
        "findings",
        "approval_boundaries",
    ]
    assert "Changed confidential claim text" not in event["payload_json"]


def test_review_feedback_taxonomy_covers_reusable_categories() -> None:
    assert set(REVIEW_FEEDBACK_CATEGORIES) == {
        "missing_evidence",
        "wrong_boundary",
        "weak_eval",
        "wrong_integration",
        "unclear_risk",
        "unsupported_claim",
    }


def test_review_feedback_records_category_without_raw_confidential_text(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    audit_events = AuditEventRepository(connection)
    raw_summary = "Client said the private renewal workflow depends on account ACME-123."

    feedback = record_review_feedback(
        run_id="run-1",
        blueprint_version_id=7,
        category="missing_evidence",
        section="integration_map",
        reviewer_label="operator",
        summary=raw_summary,
        evidence_reference=EvidenceReference(source_id="src-1", chunk_id="chk-1"),
        audit_events=audit_events,
        recorded_at="2026-05-20T00:00:00+00:00",
    )

    assert feedback.category == "missing_evidence"
    assert feedback.summary == raw_summary
    event = audit_events.list_events("run-1")[0]
    payload = json.loads(event["payload_json"])
    assert event["event_type"] == "review_feedback_recorded"
    assert payload == {
        "blueprint_version_id": 7,
        "category": "missing_evidence",
        "evidence_reference": {"chunk_id": "chk-1", "source_id": "src-1"},
        "reviewer_label": "operator",
        "section": "integration_map",
    }
    assert raw_summary not in event["payload_json"]
    assert "ACME-123" not in event["payload_json"]


def test_review_feedback_analytics_excludes_raw_review_text() -> None:
    raw_summary = "Private account ACME-123 needs extra evidence from Jane."
    feedback = [
        ReviewFeedback(
            feedback_id="fb-1",
            blueprint_version_id=1,
            category="missing_evidence",
            section="integration_map",
            reviewer_label="operator",
            summary=raw_summary,
        ),
        ReviewFeedback(
            feedback_id="fb-2",
            blueprint_version_id=1,
            category="weak_eval",
            section="eval_cases",
            reviewer_label="operator",
            summary="Expected behavior is not measurable.",
        ),
        ReviewFeedback(
            feedback_id="fb-3",
            blueprint_version_id=2,
            category="missing_evidence",
            section="integration_map",
            reviewer_label="operator",
            summary="Another confidential reviewer note.",
        ),
    ]

    analytics = summarize_review_feedback(feedback)
    payload = analytics.model_dump(mode="json")

    assert payload == {
        "total_count": 3,
        "by_category": {"missing_evidence": 2, "weak_eval": 1},
        "by_section": {"eval_cases": 1, "integration_map": 2},
        "by_blueprint_version_id": {"1": 2, "2": 1},
    }
    assert raw_summary not in json.dumps(payload)
    assert "ACME-123" not in json.dumps(payload)
