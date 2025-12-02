import typer

from cli.commands.init import InitCommand
from cli.commands.profile import ProfileCommand
from cli.commands.solve import SolveCommand
from cli.commands.submit import SubmitCommand
from cli.utils.arguments.day import Day
from cli.utils.arguments.part import PartArg
from cli.utils.context import ContextObject
from cli.utils.options.cut_off_time import CutOffTime
from cli.utils.options.force_rerun import ForceRerun
from cli.utils.options.input_file_name import InputFileName
from cli.utils.options.output_file_name import OutputFileName
from cli.utils.options.run_count import RunCount

cli = typer.Typer(help="CLI for AoC", no_args_is_help=True)


@cli.command()
def init(ctx: typer.Context, day: Day):
    """Initialize new directory for solving the queried day."""
    try:
        context = ContextObject.from_context(ctx)
        InitCommand(context=context, day=day).run()
    except Exception as e:
        print(f"failed to init: {e}")
        raise typer.Exit(1)


@cli.command()
def solve(ctx: typer.Context, day: Day, part: PartArg, input_file_name: InputFileName = "input.txt"):
    """Return answer to the requested part with the given input choice."""
    try:
        context = ContextObject.from_context(ctx)
        SolveCommand(context=context, day=day, part=part.to_part(), input_file_name=input_file_name).run()
    except Exception as e:
        print(f"failed to solve: {e}")
        raise typer.Exit(1)


@cli.command()
def submit(ctx: typer.Context, day: Day, part: PartArg):
    """Submit solution of given part to AoC."""
    try:
        context = ContextObject.from_context(ctx)
        SubmitCommand(context=context, day=day, part=part.to_part()).run()
    except Exception as e:
        print(f"failed to submit: {e}")
        raise typer.Exit(1)


@cli.command()
def profile(
    ctx: typer.Context,
    day: Day,
    run_count: RunCount = 10,
    cut_off_time: CutOffTime = 30,
    output_file_name: OutputFileName = "profiling.json",
    force_rerun: ForceRerun = False,
):
    """Profile the solutions for the queried day."""
    try:
        context = ContextObject.from_context(ctx)
        ProfileCommand(
            context=context,
            day=day,
            run_count=run_count,
            cut_off_time=cut_off_time,
            output_file_name=output_file_name,
            force_rerun=force_rerun,
        ).run()
    except Exception as e:
        print(f"failed to profile solution: {e}")
        raise typer.Exit(1)
