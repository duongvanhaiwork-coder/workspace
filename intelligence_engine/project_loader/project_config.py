from pathlib import Path
from pydantic import BaseModel, Field

class ProjectConfig(BaseModel):
    name: str
    path: str
    languages: list[str] = Field(default_factory=list)
    exclude: list[str] = Field(default_factory=lambda: [".git", "node_modules", "dist", "build"])

    def resolved_path(self, base_dir: Path | None = None) -> Path:
        p = Path(self.path)
        return p if p.is_absolute() else (base_dir or Path.cwd()) / p

class ProjectsFile(BaseModel):
    projects: list[ProjectConfig]
