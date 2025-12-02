from typing import Annotated

import typer

CutOffTime = Annotated[float, typer.Option(help="upper limit in seconds for total time usage on profiling a solution")]
