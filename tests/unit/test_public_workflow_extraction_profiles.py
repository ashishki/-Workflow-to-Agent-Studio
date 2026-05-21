from workflow_agent_studio.extraction.public_workflows import (
    PUBLIC_WORKFLOW_EXTRACTION_PROFILES,
    public_workflow_profile_for_text,
)
from workflow_agent_studio.patterns import BLUEPRINT_PROFILES


def test_public_workflow_extraction_profiles_cover_public_corpus() -> None:
    assert [profile.profile_id for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES] == [
        "kubernetes_issue_triage",
        "openstack_bug_triage",
        "gitlab_incident_workflow",
        "netbox_issue_triage",
    ]
    assert PUBLIC_WORKFLOW_EXTRACTION_PROFILES[0].steps
    assert PUBLIC_WORKFLOW_EXTRACTION_PROFILES[0].missing_questions
    assert {profile.workflow_kind for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES} <= set(
        BLUEPRINT_PROFILES
    )


def test_public_workflow_profile_detection_prefers_specific_profiles() -> None:
    kubernetes = public_workflow_profile_for_text(
        "Kubernetes GitHub Issues need issue triage with SIG ownership."
    )
    openstack = public_workflow_profile_for_text(
        "OpenStack Bug Triage uses Launchpad and bug supervisor review."
    )
    gitlab = public_workflow_profile_for_text(
        "GitLab incident workflow uses Incident.io and PagerDuty."
    )
    netbox = public_workflow_profile_for_text(
        "GitHub Issues issue triage uses templates and maintainer review."
    )

    assert kubernetes is not None
    assert kubernetes.profile_id == "kubernetes_issue_triage"
    assert kubernetes.workflow_kind == "kubernetes_issue_triage"
    assert openstack is not None
    assert openstack.profile_id == "openstack_bug_triage"
    assert openstack.workflow_kind == "bug_triage"
    assert gitlab is not None
    assert gitlab.profile_id == "gitlab_incident_workflow"
    assert gitlab.workflow_kind == "incident_response"
    assert netbox is not None
    assert netbox.profile_id == "netbox_issue_triage"
    assert netbox.workflow_kind == "issue_triage"
