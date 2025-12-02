from typing import Annotated

import typer

OutputFileName = Annotated[str, typer.Option("--output", "-o", help="file name for output file")]
