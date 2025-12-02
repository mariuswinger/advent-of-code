import requests
from bs4 import BeautifulSoup
from requests.models import Response
from rich import print

from cli.utils.arguments.day import Day
from cli.utils.command_base import CommandBase
from cli.utils.context import ContextObject
from cli.utils.part import Part
from utilities.solution_abstract import SolutionAbstract


class SubmitCommand(CommandBase):
    day: Day
    part: Part

    @property
    def solution_instance(self) -> SolutionAbstract:
        """Return solution instance."""
        return self.get_solution_instance(day=self.day, input_file_name="input.txt")

    def __init__(self, context: ContextObject, day: Day, part: Part):
        super().__init__(context=context)
        self.day = day
        self.part = part

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
        return requests.post(url, cookies={"session": self._context.session_token}, data=data)

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
