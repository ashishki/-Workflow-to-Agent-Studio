import workflow_agent_studio


def test_package_imports_with_version() -> None:
    assert isinstance(workflow_agent_studio.__version__, str)
    assert workflow_agent_studio.__version__
