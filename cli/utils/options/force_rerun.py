from typing import Annotated

import typer

ForceRerun = Annotated[bool, typer.Option("--force-rerun", "-f", help="rerun profiling")]
