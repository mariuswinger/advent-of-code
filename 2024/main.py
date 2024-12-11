import typer
from typing_extensions import Annotated
from rich import print
from utils import Part, get_day_dir_path, get_solution_function, is_valid_day, profile_solution, submit_solution

app = typer.Typer()


@app.command()
def test(day: int, part: Part):
    _validate_day(day)
    print(f"[SAMPLE INPUT] solving day {day}, part {part.value}:")
    solution_function = get_solution_function(day, part, use_sample_input=True)
    answer = solution_function()
    print(f"answer: {answer}")


@app.command()
def solve(day: int, part: Part):
    _validate_day(day)
    print(f"solving day {day}, part {part.value}:")
    solution_function = get_solution_function(day, part)
    answer = solution_function()
    print(f"answer: {answer}")


@app.command()
def profile(day: int, runcount: Annotated[int, typer.Option(help="number of times to run code")] = 10):
    _validate_day(day)
    print(f"profiling solution for day {day}:")
    output_filepath = get_day_dir_path(day) / "analysis.txt"
    times_part_a = profile_solution(get_solution_function(day, Part.A), runcount)
    times_part_b = profile_solution(get_solution_function(day, Part.B), runcount)
    results = [
        f"Results for day {day}, part A (N={runcount}):\n"
        f"ran the code a total of {runcount} time(s)\n"
        f" average time: {times_part_a.mean()}\n"
        f" max time:     {times_part_a.max()}\n"
        f" min time:     {times_part_a.min()}\n\n"
        f"Results for day {day}, part B (N={runcount}):\n"
        f"ran the code a total of {runcount} time(s)\n"
        f" average time: {times_part_b.mean()}\n"
        f" max time:     {times_part_b.max()}\n"
        f" min time:     {times_part_b.min()}\n"
    ]
    with output_filepath.open("w") as file:
        file.writelines(results)
    for line in results:
        print(line)


@app.command()
def submit(day: int, part: Part):
    _validate_day(day)
    print(f"solving day {day}, part {part.value}:")
    solution_function = get_solution_function(day, part)
    answer = solution_function()
    submit_solution(day, part, answer)


def _validate_day(day: int) -> None:
    if not is_valid_day(day):
        print("error: 'day' must be in range 1-25")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
