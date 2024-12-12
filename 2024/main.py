import typer

from cli.init import app as init
from cli.profile import app as profile
from cli.solve import app as solver
from cli.submit import app as submit

app = typer.Typer()
app.add_typer(solver)
app.add_typer(init)
app.add_typer(submit)
app.add_typer(profile)


if __name__ == "__main__":
    app()
