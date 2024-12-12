import numpy as np

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    reports: list[np.ndarray]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        reports = []
        for x in self.raw_data:
            reports.append(np.array(x.split(" "), dtype=np.int32))
        self.reports = reports

    def part_a(self) -> int:
        """Solve part a."""
        safe_level_indices = []
        for i, report in enumerate(self.reports):
            if _is_safe_report(report):
                safe_level_indices.append(i)
        return len(safe_level_indices)

    def part_b(self) -> int:
        """Solve part b."""
        salvageable_level_indices = []
        for i, report in enumerate(self.reports):
            if _is_safe_report(report):
                salvageable_level_indices.append(i)
                continue
            if _is_report_salvageable(report):
                salvageable_level_indices.append(i)
        return len(salvageable_level_indices)


def _is_safe_report(report: np.ndarray) -> bool:
    """Return True if report is deemed safe."""
    report_diff = np.diff(report)
    zero_jumps = report_diff == 0
    if np.sum(zero_jumps) > 0:
        return False
    if not np.all(np.diff(np.sign(report_diff)) == 0):
        return False
    report_jump_lengths = np.abs(report_diff)
    if np.any(report_jump_lengths > 3):
        return False
    return True


def _is_report_salvageable(report: np.ndarray) -> bool:
    """Return True if report can be salvaged."""
    mask = np.ones(report.shape, dtype=bool)
    for i in range(len(report)):
        mask[i] = 0
        if _is_safe_report(report[mask]):
            mask[i] = 1
            return True
        mask[i] = 1
    return False
