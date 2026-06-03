from intelligence_engine.project_loader.project_config import ProjectConfig

def test_project_config():
    p = ProjectConfig(name="x", path=".")
    assert p.name == "x"
