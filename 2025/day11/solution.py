from day11.utils.count_paths import count_paths

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    adjacency_list: dict[str, str]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        adjacency_list = {}
        for line in self.raw_data:
            identifier, edges = line.split(": ")
            adjacency_list[identifier] = edges.split()
        self.adjacency_list = adjacency_list

    def part_a(self) -> int:
        """Solve part a."""
        return count_paths(current="you", target="out", adjacency_list=self.adjacency_list, memoized_path_counts={})

    def part_b(self) -> int:
        """Solve part b."""
        paths_from_fft_to_dac = count_paths(
            current="fft", target="dac", adjacency_list=self.adjacency_list, memoized_path_counts={}
        )

        # either fft -> dac or dac -> fft
        if paths_from_fft_to_dac > 0:
            paths_from_svr_to_fft = count_paths(
                current="svr", target="fft", adjacency_list=self.adjacency_list, memoized_path_counts={}
            )
            paths_from_dac_to_out = count_paths(
                current="dac", target="out", adjacency_list=self.adjacency_list, memoized_path_counts={}
            )
            return paths_from_svr_to_fft * paths_from_fft_to_dac * paths_from_dac_to_out
        else:
            paths_from_svr_to_dac = count_paths(
                current="svr", target="dac", adjacency_list=self.adjacency_list, memoized_path_counts={}
            )
            paths_from_dac_to_fft = count_paths(
                current="dac", target="fft", adjacency_list=self.adjacency_list, memoized_path_counts={}
            )
            paths_from_fft_to_out = count_paths(
                current="fft", target="out", adjacency_list=self.adjacency_list, memoized_path_counts={}
            )
            return paths_from_svr_to_dac * paths_from_dac_to_fft * paths_from_fft_to_out
