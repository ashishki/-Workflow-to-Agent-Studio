import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.domain.workflow import WorkflowStep

FIXTURE_PATH = Path("tests/fixtures/blueprints/minimal_valid.json")


def _minimal_blueprint_data() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_minimal_blueprint_fixture_validates() -> None:
    blueprint = AutomationBlueprint.model_validate(_minimal_blueprint_data())

    assert blueprint.schema_version == "v1"
    assert blueprint.workflow_summary.text
    assert blueprint.actors
    assert blueprint.systems
    assert blueprint.current_workflow_steps
    assert blueprint.automation_candidates
    assert blueprint.eval_cases
    assert blueprint.next_implementation_tasks


def test_claim_requires_evidence_or_assumption() -> None:
    data = copy.deepcopy(_minimal_blueprint_data())
    data["workflow_summary"] = {"text": "Unsupported claim"}

    with pytest.raises(ValidationError, match="claim requires evidence"):
        AutomationBlueprint.model_validate(data)


def test_blueprint_schema_version_serializes() -> None:
    blueprint = AutomationBlueprint.model_validate(_minimal_blueprint_data())

    assert blueprint.model_dump(mode="json")["schema_version"] == "v1"


def test_workflow_step_requires_evidence_or_assumption() -> None:
    with pytest.raises(ValidationError, match="workflow step requires evidence"):
        WorkflowStep(step_id="step-1", description="Review the request.", actor="Operator")
