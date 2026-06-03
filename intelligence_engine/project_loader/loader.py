import json
from pathlib import Path
from .project_config import ProjectConfig, ProjectsFile

class ProjectLoader:
    def __init__(self, projects_file: str | Path = "projects.json") -> None:
        self.projects_file = Path(projects_file)

    def load_all(self) -> list[ProjectConfig]:
        if not self.projects_file.exists():
            raise FileNotFoundError(f"projects file not found: {self.projects_file}")
        data = json.loads(self.projects_file.read_text(encoding="utf-8"))
        return ProjectsFile(**data).projects

    def get(self, name: str) -> ProjectConfig:
        for project in self.load_all():
            if project.name == name:
                return project
        raise KeyError(f"project not found: {name}")
