from workflow_agent_studio.domain.workflow import WorkflowKind
from workflow_agent_studio.extraction.public_workflows import (
    PUBLIC_WORKFLOW_EXTRACTION_PROFILES,
    public_workflow_profile_for_text,
)
from workflow_agent_studio.patterns import BLUEPRINT_PROFILES


def test_public_workflow_extraction_profiles_cover_public_corpus() -> None:
    assert [profile.profile_id for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES] == [
        "apache_airflow_issue_triage",
        "django_ticket_triage",
        "kubernetes_issue_triage",
        "openstack_bug_triage",
        "mozilla_bugzilla_triage",
        "gitlab_incident_workflow",
        "hvac_lead_intake",
        "netbox_issue_triage",
    ]
    assert PUBLIC_WORKFLOW_EXTRACTION_PROFILES[0].steps
    assert PUBLIC_WORKFLOW_EXTRACTION_PROFILES[0].missing_questions
    assert {profile.workflow_kind for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES} <= set(
        BLUEPRINT_PROFILES
    )
    workflow_kind: WorkflowKind = PUBLIC_WORKFLOW_EXTRACTION_PROFILES[2].workflow_kind
    assert workflow_kind == "kubernetes_issue_triage"


def test_public_workflow_profile_detection_prefers_specific_profiles() -> None:
    kubernetes = public_workflow_profile_for_text(
        "Kubernetes GitHub Issues need issue triage with SIG ownership."
    )
    airflow = public_workflow_profile_for_text(
        "Apache Airflow issue triage team converts reports to GitHub Discussions."
    )
    django = public_workflow_profile_for_text(
        "Django Trac ticket triage reviews ticket stages and ready for checkin flags."
    )
    openstack = public_workflow_profile_for_text(
        "OpenStack Bug Triage uses Launchpad and bug supervisor review."
    )
    mozilla = public_workflow_profile_for_text(
        "Mozilla Bugzilla triage uses whiteboard tags and needinfo follow-up."
    )
    gitlab = public_workflow_profile_for_text(
        "GitLab incident workflow uses Incident.io and PagerDuty."
    )
    hvac = public_workflow_profile_for_text(
        "HVAC service-area appointment workflow captures service type and urgency."
    )
    netbox = public_workflow_profile_for_text(
        "GitHub Issues issue triage uses templates and maintainer review."
    )

    assert kubernetes is not None
    assert kubernetes.profile_id == "kubernetes_issue_triage"
    assert kubernetes.workflow_kind == "kubernetes_issue_triage"
    assert airflow is not None
    assert airflow.profile_id == "apache_airflow_issue_triage"
    assert airflow.workflow_kind == "apache_airflow_issue_triage"
    assert django is not None
    assert django.profile_id == "django_ticket_triage"
    assert django.workflow_kind == "django_ticket_triage"
    assert openstack is not None
    assert openstack.profile_id == "openstack_bug_triage"
    assert openstack.workflow_kind == "bug_triage"
    assert mozilla is not None
    assert mozilla.profile_id == "mozilla_bugzilla_triage"
    assert mozilla.workflow_kind == "mozilla_bugzilla_triage"
    assert gitlab is not None
    assert gitlab.profile_id == "gitlab_incident_workflow"
    assert gitlab.workflow_kind == "incident_response"
    assert hvac is not None
    assert hvac.profile_id == "hvac_lead_intake"
    assert hvac.workflow_kind == "hvac_lead_intake"
    assert netbox is not None
    assert netbox.profile_id == "netbox_issue_triage"
    assert netbox.workflow_kind == "issue_triage"
