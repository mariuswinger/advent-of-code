import typer
from typing_extensions import Annotated

Day = Annotated[int, typer.Argument(min=1, max=25)]
