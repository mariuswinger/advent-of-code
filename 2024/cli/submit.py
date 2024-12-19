import requests
import typer
from bs4 import BeautifulSoup
from requests.models import Response
from rich import print

from cli.utils.abstract_command import CommandBase
from cli.utils.day import Day
from cli.utils.part import Part, PartArg
from utilities.solution_abstract import SolutionAbstract

app = typer.Typer()


class SubmitCommand(CommandBase):
    day: Day
    part: Part
    solution_instance: SolutionAbstract

    def __init__(self, day: Day, part: Part):
        super().__init__()
        self.day = day
        self.part = part
        self.solution_instance = self.get_solution_instance(self.day, input_file_name="input.txt")

    def run(self) -> None:
        """Submit solution of given part to AoC."""
        print(f"AoC-{self.year}, day {self.day}, part {self.part}")
        print("computing answer value ...")
        answer = self.solution_instance.solve(self.part)

        print(f"submitting answer value '{answer}' ...")
        response = self._post_request(answer)
        if response.status_code != 200:
            raise ValueError(f"unexpected response code: {response.status_code}")

        parsed_response = self._parse_response(response.text)
        print(f"response from AoC: {parsed_response}")

    def _post_request(self, answer: int) -> Response:
        """Post results to AoC."""
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"
        data = {"level": str(self.part), "answer": str(answer)}
        return requests.post(url, cookies={"session": self.session_token}, data=data)

    @staticmethod
    def _parse_response(response_text: str) -> str:
        """Parse response received from AoC."""
        soup = BeautifulSoup(response_text, "html.parser")
        main = soup.main
        if main is None:
            raise ValueError("could not find main tag in response")
        article = main.article
        if article is None:
            raise ValueError("could not find main.article tag in response")
        output = article.p
        if output is None:
            raise ValueError("could not find main.article.p tag in response")

        if "That's the right answer!" in output.text:
            return f"[green]{output.text}[/green]"
        elif "You don't seem to be solving the right level." in output.text:
            return f"[yellow]{output.text}[/yellow]"
        elif "You gave an answer too recently" in output.text:
            return f"[yellow]{output.text}[/yellow]"
        else:
            return f"[red]{output.text}[/red]"


@app.command()
def submit(
    day: Day,
    part: PartArg,
):
    """Submit solution of given part to AoC."""
    try:
        SubmitCommand(day=day, part=part.to_part()).run()
    except Exception as e:
        print(f"failed to submit: {e}")
        raise typer.Exit(1)
