from utilities.types import Index2D


def run_dfs(start: Index2D, plant_graph: dict[Index2D, set[Index2D]]) -> set[Index2D]:
    region = set()
    _dfs_main_loop(current_node=start, region=region, graph=plant_graph)
    return region


def _dfs_main_loop(
    current_node: Index2D,
    region: set[Index2D],
    graph: dict[Index2D, set[Index2D]],
):
    if current_node in region:
        return
    region.add(current_node)

    for neighbour in graph[current_node]:
        _dfs_main_loop(
            current_node=neighbour,
            region=region,
            graph=graph,
        )
