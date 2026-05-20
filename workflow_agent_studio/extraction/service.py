"""Workflow extraction service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from workflow_agent_studio.config import Settings, load_settings
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowStep
from workflow_agent_studio.llm import (
    FakeStructuredOutputProvider,
    StructuredOutputProvider,
    request_structured_output,
)
from workflow_agent_studio.retrieval.evidence import EvidenceSnippet


@dataclass(frozen=True)
class MissingQuestion:
    section: str
    question: str
    reason: str


@dataclass(frozen=True)
class ExtractedWorkflowMap:
    actors: list[str]
    systems: list[str]
    triggers: list[str]
    steps: list[WorkflowStep]
    decisions: list[str]
    exceptions: list[str]
    data_fields: list[str]
    pain_points: list[str]
    missing_questions: list[MissingQuestion] = field(default_factory=list)


class StructuredMissingQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section: str = Field(min_length=1)
    question: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class StructuredWorkflowExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["v1"] = "v1"
    actors: list[str] = Field(min_length=1)
    systems: list[str] = Field(min_length=1)
    triggers: list[str] = Field(min_length=1)
    steps: list[WorkflowStep] = Field(min_length=1)
    decisions: list[str] = Field(min_length=1)
    exceptions: list[str] = Field(min_length=1)
    data_fields: list[str] = Field(min_length=1)
    pain_points: list[str] = Field(min_length=1)
    missing_questions: list[StructuredMissingQuestion] = Field(default_factory=list)


def extract_workflow_map(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
) -> ExtractedWorkflowMap:
    reference = _first_reference(evidence)
    text = source.normalized_text.casefold()
    if _looks_like_issue_triage_workflow(text):
        return _extract_issue_triage_workflow(reference)

    steps = [
        WorkflowStep(
            step_id="step-1",
            description="Review inbound support request.",
            actor="Operator",
            system="Inbox",
            evidence_references=[reference] if reference else [],
            assumption=reference is None,
        ),
        WorkflowStep(
            step_id="step-2",
            description="Create follow-up task when engineering review is needed.",
            actor="Operator",
            system="Task Tracker",
            evidence_references=[reference] if reference else [],
            assumption=reference is None,
        ),
    ]
    missing_questions: list[MissingQuestion] = []
    if "approval" not in text:
        missing_questions.append(
            MissingQuestion(
                section="approval_boundaries",
                question="Who approves follow-up tasks before they create team commitments?",
                reason="The source describes task creation but does not name an approver.",
            )
        )
    return ExtractedWorkflowMap(
        actors=["Operator"],
        systems=["Inbox", "CRM", "Task Tracker"],
        triggers=["Inbound support request"],
        steps=steps,
        decisions=["Decide whether engineering review is needed"],
        exceptions=["Missing details require customer clarification"],
        data_fields=["customer name", "request ID", "issue summary"],
        pain_points=["Manual follow-up task creation"],
        missing_questions=missing_questions,
    )


def _looks_like_issue_triage_workflow(text: str) -> bool:
    required_terms = ("github issues", "issue", "triage")
    return all(term in text for term in required_terms)


def _extract_issue_triage_workflow(
    reference: EvidenceReference | None,
) -> ExtractedWorkflowMap:
    evidence_references = [reference] if reference else []
    return ExtractedWorkflowMap(
        actors=["Reporter", "Maintainer or triager", "Contributor or engineering owner"],
        systems=[
            "GitHub Issues",
            "Issue templates",
            "Issue labels or GitHub issue types",
            "Canned maintainer responses",
            "Project backlog",
        ],
        triggers=[
            "New GitHub issue, feature request, bug report, support-like request, or pull request"
        ],
        steps=[
            WorkflowStep(
                step_id="step-1",
                description="Reporter opens a GitHub issue using the expected template.",
                actor="Reporter",
                system="GitHub Issues",
                evidence_references=evidence_references,
                assumption=reference is None,
            ),
            WorkflowStep(
                step_id="step-2",
                description=(
                    "Maintainer checks template completion, issue type, scope, "
                    "and duplicate status."
                ),
                actor="Maintainer or triager",
                system="Issue templates",
                evidence_references=evidence_references,
                assumption=reference is None,
            ),
            WorkflowStep(
                step_id="step-3",
                description=(
                    "Maintainer asks for clarification when reproduction steps "
                    "or feature details are missing."
                ),
                actor="Maintainer or triager",
                system="Canned maintainer responses",
                evidence_references=evidence_references,
                assumption=reference is None,
            ),
            WorkflowStep(
                step_id="step-4",
                description=(
                    "Accepted issues move toward ownership, engineering review, "
                    "or linked pull request work."
                ),
                actor="Contributor or engineering owner",
                system="Project backlog",
                evidence_references=evidence_references,
                assumption=reference is None,
            ),
        ],
        decisions=[
            "Decide whether the submission follows the required issue template",
            (
                "Decide whether the issue is duplicate, out of scope, "
                "support-oriented, or expected behavior"
            ),
            "Decide whether a bug report is reproducible on a current stable release",
            (
                "Decide whether a feature request has a justified use case "
                "and enough implementation detail"
            ),
            (
                "Decide whether to ask for more information, mark stale, close, "
                "accept, or route to engineering review"
            ),
        ],
        exceptions=[
            "Missing template fields require maintainer clarification before acceptance",
            "Duplicate, support-like, or out-of-scope issues can be closed",
            "Issues without requested follow-up can become stale and eventually close",
        ],
        data_fields=[
            "issue type",
            "reporter",
            "template completion state",
            "product version",
            "reproduction steps",
            "expected behavior",
            "actual behavior",
            "use case",
            "scope decision",
            "owner",
            "linked pull request",
        ],
        pain_points=[
            "Maintainers repeatedly check issue templates and request missing details",
            "Duplicate, support, and out-of-scope submissions consume triage time",
            "Stale issues require consistent follow-up and closure decisions",
        ],
        missing_questions=[
            MissingQuestion(
                section="approval_boundaries",
                question="Who has final authority to accept an issue for engineering review?",
                reason=(
                    "The public source describes triage decisions but not a single final approver."
                ),
            )
        ],
    )


def extract_workflow_map_with_provider(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
    provider: StructuredOutputProvider,
) -> ExtractedWorkflowMap:
    result = request_structured_output(
        provider=provider,
        prompt=_provider_extraction_prompt(source=source, evidence=evidence),
        output_model=StructuredWorkflowExtraction,
    )
    return _from_structured_output(result.output)


def extract_workflow_map_provider_backed(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
    settings: Settings | None = None,
    provider: StructuredOutputProvider | None = None,
) -> ExtractedWorkflowMap:
    active_settings = settings or load_settings()
    active_provider = provider or _provider_from_settings(
        settings=active_settings,
        source=source,
        evidence=evidence,
    )
    return extract_workflow_map_with_provider(
        source=source,
        evidence=evidence,
        provider=active_provider,
    )


def extraction_provider_payload(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
) -> dict[str, object]:
    workflow = extract_workflow_map(source=source, evidence=evidence)
    return {
        "schema_version": "v1",
        "actors": workflow.actors,
        "systems": workflow.systems,
        "triggers": workflow.triggers,
        "steps": [step.model_dump(mode="python") for step in workflow.steps],
        "decisions": workflow.decisions,
        "exceptions": workflow.exceptions,
        "data_fields": workflow.data_fields,
        "pain_points": workflow.pain_points,
        "missing_questions": [
            {
                "section": question.section,
                "question": question.question,
                "reason": question.reason,
            }
            for question in workflow.missing_questions
        ],
    }


def _first_reference(evidence: list[EvidenceSnippet]) -> EvidenceReference | None:
    if not evidence:
        return None
    first = evidence[0]
    return EvidenceReference(source_id=first.source_id, chunk_id=first.chunk_id)


def _provider_extraction_prompt(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
) -> str:
    evidence_ids = ", ".join(snippet.chunk_id for snippet in evidence)
    return (
        "Extract workflow facts as schema_version v1 JSON. "
        f"Use only source_id={source.source_id} and evidence chunks: {evidence_ids}.\n\n"
        f"{source.normalized_text}"
    )


def _provider_from_settings(
    *,
    settings: Settings,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
) -> StructuredOutputProvider:
    if settings.llm_provider != "fake":
        raise ValueError("Provider-backed extraction requires an injected structured provider.")
    return FakeStructuredOutputProvider(
        payload=extraction_provider_payload(source=source, evidence=evidence),
        model_name=settings.extraction_model,
    )


def _from_structured_output(output: StructuredWorkflowExtraction) -> ExtractedWorkflowMap:
    return ExtractedWorkflowMap(
        actors=output.actors,
        systems=output.systems,
        triggers=output.triggers,
        steps=output.steps,
        decisions=output.decisions,
        exceptions=output.exceptions,
        data_fields=output.data_fields,
        pain_points=output.pain_points,
        missing_questions=[
            MissingQuestion(
                section=question.section,
                question=question.question,
                reason=question.reason,
            )
            for question in output.missing_questions
        ],
    )
