from dataclasses import dataclass
from pathlib import Path
from typing import Self

import typer

from cli.utils.year_directory import YearDirectory


@dataclass
class ContextObject:
    year: int
    project_root: Path
    session_token: str

    @property
    def year_directory(self) -> YearDirectory:
        """Return directory to the selected year."""
        return YearDirectory(self.project_root / str(self.year))

    @property
    def template_file(self) -> Path:
        """Return path to template solution."""
        return self.project_root / "cli/utils/solution_template.py"

    @classmethod
    def from_context(cls, ctx: typer.Context) -> Self:
        """Create from typer.Context."""
        return cls(
            year=ctx.obj["year"],
            project_root=ctx.obj["project_root"],
            session_token=ctx.obj["session_token"],
        )
