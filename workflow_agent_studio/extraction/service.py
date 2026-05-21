"""Workflow extraction service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from workflow_agent_studio.config import Settings, load_settings
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowStep
from workflow_agent_studio.extraction.public_workflows import (
    PublicWorkflowExtractionProfile,
    public_workflow_profile_for_text,
)
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
    public_profile = public_workflow_profile_for_text(source.normalized_text)
    if public_profile is not None:
        return _extract_public_workflow_profile(public_profile, reference)

    return _extract_support_intake_workflow(source=source, reference=reference)


def _extract_support_intake_workflow(
    *,
    source: SourceDocument,
    reference: EvidenceReference | None,
) -> ExtractedWorkflowMap:
    evidence_references = _evidence_references(reference)
    steps = [
        WorkflowStep(
            step_id="step-1",
            description="Review inbound support request.",
            actor="Operator",
            system="Inbox",
            evidence_references=evidence_references,
            assumption=reference is None,
        ),
        WorkflowStep(
            step_id="step-2",
            description="Create follow-up task when engineering review is needed.",
            actor="Operator",
            system="Task Tracker",
            evidence_references=evidence_references,
            assumption=reference is None,
        ),
    ]
    missing_questions: list[MissingQuestion] = []
    if "approval" not in source.normalized_text.casefold():
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


def _extract_public_workflow_profile(
    profile: PublicWorkflowExtractionProfile,
    reference: EvidenceReference | None,
) -> ExtractedWorkflowMap:
    evidence_references = _evidence_references(reference)
    return ExtractedWorkflowMap(
        actors=list(profile.actors),
        systems=list(profile.systems),
        triggers=list(profile.triggers),
        steps=[
            WorkflowStep(
                step_id=step.step_id,
                description=step.description,
                actor=step.actor,
                system=step.system,
                evidence_references=evidence_references,
                assumption=reference is None,
            )
            for step in profile.steps
        ],
        decisions=list(profile.decisions),
        exceptions=list(profile.exceptions),
        data_fields=list(profile.data_fields),
        pain_points=list(profile.pain_points),
        missing_questions=[
            MissingQuestion(
                section=question.section,
                question=question.question,
                reason=question.reason,
            )
            for question in profile.missing_questions
        ],
    )


def _evidence_references(reference: EvidenceReference | None) -> list[EvidenceReference]:
    return [reference] if reference else []


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
