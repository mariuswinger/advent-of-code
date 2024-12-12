from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    comes_before: dict[int, set[int]]
    update_page_numbers: list[list[int]]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        break_index = self.raw_data.index("")
        page_ordering_rules = [(int(p.split("|")[0]), int(p.split("|")[1])) for p in self.raw_data[:break_index]]
        comes_before = {}
        for before_page, after_page in page_ordering_rules:
            if before_page not in comes_before:
                comes_before[before_page] = {after_page}
            else:
                comes_before[before_page].add(after_page)
        self.comes_before = {k: comes_before[k] for k in sorted(comes_before)}
        self.update_page_numbers = [list(map(int, line.split(","))) for line in self.raw_data[break_index + 1 :]]

    def part_a(self) -> int:
        """Solve part a."""
        sum = 0
        for update in self.update_page_numbers:
            if _is_ordered(self.comes_before, update):
                sum += update[len(update) // 2]
        return sum

    def part_b(self) -> int:
        """Solve part b."""
        incorrect_update_indices = []

        for update_index, update in enumerate(self.update_page_numbers):
            if not _is_ordered(self.comes_before, update):
                incorrect_update_indices.append(update_index)

        sum = 0
        for i in incorrect_update_indices:
            incorrect_update = set(self.update_page_numbers[i])
            update_length = len(incorrect_update)
            for k in incorrect_update:
                priority = len(incorrect_update.intersection(self.comes_before[k]))
                if priority == update_length // 2:
                    sum += k
        return sum


def _is_ordered(comes_before: dict[int, set[int]], update: list[int]) -> bool:
    """Return True if the update is ordered correctly."""
    for page_index, page in enumerate(update):
        if page_index == len(update) - 1:
            # if at the last page, we are good
            return True
        if page not in comes_before:
            # invalid update since we are not at last page
            return False
        if update[page_index + 1] not in comes_before[page]:
            return False
    return True
