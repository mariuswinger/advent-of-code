from pathlib import Path
from typing import Annotated

import typer


def input_file_name_callback(input_file_name: str):
    """Ensure that input file name has suffix."""
    if Path(input_file_name).suffix == "":
        print(f"[yellow]input file name '{input_file_name}' has no suffix, assumes '.txt' suffix[/yellow]")
        return input_file_name + ".txt"
    return input_file_name


InputFileName = Annotated[
    str,
    typer.Option(
        "--input-file", "-i", callback=input_file_name_callback, help="filename of file to read input data from"
    ),
]
