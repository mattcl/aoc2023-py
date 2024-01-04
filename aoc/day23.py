"""23: PROBLEM NAME"""
from collections import deque
from copy import deepcopy
from multiprocessing import Pool

import aoc.util


NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3


NEIGHBORS = [
    (1, 0, SOUTH),
    (0, 1, EAST),
    (-1, 0, NORTH),
    (0, -1, WEST),
]


def permitted(tile, dir) -> bool:
    match tile:
        case '.': return True
        case '^': return dir == NORTH
        case 'v': return dir == SOUTH
        case '>': return dir == EAST
        case '<': return dir == WEST
        case _: return True


def more_than_two_connections(loc, grid) -> bool:
    count = 0
    for (dr, dc, _) in NEIGHBORS:
        r = loc[0] + dr
        c = loc[1] + dc
        if not grid[r][c] == '#':
            count += 1

            if count > 2:
                return True

    return False


class Node:
    def __init__(self, idx, location):
        self.idx = idx
        self.location = location
        self.neighbors = []


def make_base_graph(grid):
    height = len(grid)
    width = len(grid[0])
    graph = []
    start = Node(0, (0, 1))
    end = Node(1, (height - 1, width - 2))
    graph.append(start)
    graph.append(end)

    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if not grid[r][c] == '#':
                loc = (r, c)
                if more_than_two_connections(loc, grid):
                    graph.append(Node(len(graph), loc))

    return graph


def populate_graph_with_slopes(base_graph, grid):
    translation = {}

    for n in base_graph:
        translation[n.location] = n.idx

    for idx in range(len(base_graph)):
        base_graph[idx].neighbors = explore_to_neighbors_with_slopes(idx, base_graph, translation, grid)


def explore_to_neighbors_with_slopes(idx, graph, translation, grid):
    height = len(grid)
    width = len(grid[0])
    out = []
    seen = set()
    start = graph[idx].location

    cur = deque()
    cur.append((start, 0))

    while len(cur) > 0:
        next = deque()
        for (loc, dist) in cur:
            if loc in seen:
                continue

            seen.add(loc)

            for (dr, dc, dir) in NEIGHBORS:
                r = loc[0] + dr
                c = loc[1] + dc

                if r < 0 or c < 0 or r >= height or c >= width:
                    continue

                nt = grid[r][c]

                if nt != '#' and permitted(nt, dir):
                    nloc = (r, c)
                    if nloc != start and nloc in translation:
                        nidx = translation[nloc]
                        out.append((nidx, dist + 1))
                    else:
                        next.append((nloc, dist + 1))

        cur = next

    return out


def populate_graph_without_slopes(base_graph, grid):
    translation = {}

    for n in base_graph:
        translation[n.location] = n.idx

    for idx in range(len(base_graph)):
        base_graph[idx].neighbors = explore_to_neighbors_without_slopes(idx, base_graph, translation, grid)


def explore_to_neighbors_without_slopes(idx, graph, translation, grid):
    height = len(grid)
    width = len(grid[0])
    out = []
    seen = set()
    start = graph[idx].location

    cur = deque()
    cur.append((start, 0))

    while len(cur) > 0:
        next = deque()
        for (loc, dist) in cur:
            if loc in seen:
                continue

            seen.add(loc)

            for (dr, dc, dir) in NEIGHBORS:
                r = loc[0] + dr
                c = loc[1] + dc

                if r < 0 or c < 0 or r >= height or c >= width:
                    continue

                nt = grid[r][c]

                if nt != '#':
                    nloc = (r, c)
                    if nloc != start and nloc in translation:
                        nidx = translation[nloc]
                        out.append((nidx, dist + 1))
                    else:
                        next.append((nloc, dist + 1))

        cur = next

    return out


def longest_distance(graph, starting_depth, pool, slope) -> int:
    # we know graph[0] exists because it's the start
    second, second_dist = graph[0].neighbors[0]

    if len(graph[1].neighbors) == 0:
        end = 1
        end_dist = 0
        initial_seen = 1 | (1 << second)
    else:
        end, end_dist = graph[1].neighbors[0]
        initial_seen = 3 | (1 << second)

    starting_points = deque()
    starting_points.append((second, second_dist + end_dist, initial_seen))

    # bfs to the starting_depth
    for _ in range(2, starting_depth):
        next = deque()
        for (idx, dist, seen) in starting_points:
            for (fidx, fdist) in graph[idx].neighbors:
                mask = 1 << fidx
                if mask & seen == 0:
                    next.append((fidx, dist + fdist, seen | mask))

        starting_points = next

    # dfs from each starting point
    args = deque()
    for (idx, dist, seen) in starting_points:
        args.append((idx, dist, end, seen))

    if slope:
        return max(pool.starmap(dfs_slope, args))
    else:
        return max(pool.starmap(dfs, args))


def dfs_slope(start, cur_cost, goal, seen) -> int:
    global sloped
    longest = [0]
    longest_recur(start, cur_cost, goal, sloped, seen, longest)
    return longest[0]


def dfs(start, cur_cost, goal, seen) -> int:
    global graph
    longest = [0]
    longest_recur(start, cur_cost, goal, graph, seen, longest)
    return longest[0]


def longest_recur(start, cur_cost, goal, graph, seen, longest):
    if start == goal:
        longest[0] = max(longest[0], cur_cost)
        return

    mask = 1 << start
    next_seen = seen | mask

    for (next_idx, dist) in graph[start].neighbors:
        if (1 << next_idx) & next_seen == 0:
            longest_recur(next_idx, cur_cost + dist, goal, graph, next_seen, longest)


def pool_init(s, g):
    global sloped
    global graph

    sloped = s
    graph = g


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        grid = input.splitlines()

        # make reduced graphs
        slope_graph = make_base_graph(grid)

        graph = deepcopy(slope_graph)

        populate_graph_with_slopes(slope_graph, grid)
        populate_graph_without_slopes(graph, grid)

        # this is hacky, but we don't have more than depth 5 to work with for
        # the example input
        if len(grid) > 100:
            # we are the real input
            depth = 10
        else:
            depth = 5

        with Pool(initializer=pool_init, initargs=[slope_graph, graph]) as pool:
            self.p1 = longest_distance(slope_graph, depth, pool, True)
            self.p2 = longest_distance(graph, depth, pool, False)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2
