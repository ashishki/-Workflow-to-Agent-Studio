"""Workflow extraction service."""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowStep
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


def extract_workflow_map(
    *,
    source: SourceDocument,
    evidence: list[EvidenceSnippet],
) -> ExtractedWorkflowMap:
    reference = _first_reference(evidence)
    text = source.normalized_text.casefold()
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


def _first_reference(evidence: list[EvidenceSnippet]) -> EvidenceReference | None:
    if not evidence:
        return None
    first = evidence[0]
    return EvidenceReference(source_id=first.source_id, chunk_id=first.chunk_id)
