def count_paths(
    current: str,
    target: str,
    adjacency_list: dict[str, str],
    memoized_path_counts: dict[str, int],
) -> int:
    if current == target:
        return 1

    # check if current is memoized
    if current in memoized_path_counts:
        return memoized_path_counts[current]

    total = 0
    neighbours = adjacency_list.get(current, [])
    for neighbour in neighbours:
        total += count_paths(neighbour, target, adjacency_list, memoized_path_counts)

    # memoize current node
    memoized_path_counts[current] = total

    return total
