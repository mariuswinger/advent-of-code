from typing import Annotated

import typer

RunCount = Annotated[int, typer.Option(help="number of times to run code")]
