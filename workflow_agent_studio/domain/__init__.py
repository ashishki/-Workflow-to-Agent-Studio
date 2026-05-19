"""Domain schemas for Workflow-to-Agent Studio."""

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowMap

__all__ = ["AutomationBlueprint", "EvidenceReference", "SourceDocument", "WorkflowMap"]
