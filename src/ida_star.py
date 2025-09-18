from .solver import Solver
from sokoban.map import Map
from sokoban.moves import *
import math


class IDAStarSolver(Solver):
    """
    IDA* solver using Manhattan-distance heuristic for boxes.
    Iterative Deepening A* combines the memory efficiency of DFS
    with the heuristic guidance of A* by performing depth-limited searches
    using a cost threshold.
    """

    def heuristic(self, state: Map) -> int:
        """
        Heuristic function estimating cost from current state to goal.
        Computes the sum of minimum Manhattan distances from each box
        to the nearest target. Admissible and consistent in grid-based maps.
        """
        total = 0
        for (box_x, box_y) in state.positions_of_boxes:
            dmin = math.inf
            for (tx, ty) in state.targets:
                d = abs(box_x - tx) + abs(box_y - ty)
                if d < dmin:
                    dmin = d
            total += dmin
        return total

    def solve(self) -> list[int] | None:
        """
        Performs the IDA* search, returning a list of moves if a solution is found.
        If no solution exists, returns None.
        """
        start = self.map.copy()
        bound = self.heuristic(start)  # initial threshold based on heuristic
        start_key = str(start)

        def dfs(state: Map, g: int, bound: int, visited: set[str]) -> tuple[bool | int, list[int] | None]:
            """
            Recursive depth-first search with cost-bound pruning.
            Returns:
                - (True, path) if goal is found
                - (next_threshold, None) if current path exceeds bound
            """
            f = g + self.heuristic(state)
            if f > bound:
                return f, None  # cut off this branch
            if state.is_solved():
                return True, []  # goal reached

            min_t = math.inf  # minimum cost encountered above current bound

            for move in state.filter_possible_moves():
                nxt = state.copy()
                nxt.apply_move(move)
                key = str(nxt)

                if key in visited:
                    continue  # avoid cycles

                visited.add(key)
                t, path = dfs(nxt, g + 1, bound, visited)
                visited.remove(key)

                if t is True:
                    return True, [move] + path  # propagate solution path

                if isinstance(t, int) and t < min_t:
                    min_t = t  # update next threshold for next iteration

            return min_t, None

        # Iteratively deepen the search with increasing threshold
        while True:
            visited = {start_key}
            t, path = dfs(start, 0, bound, visited)

            if t is True:
                return path  # solution found

            if path is not None:
                return path  # defensive, should be redundant

            if t == math.inf:
                return None  # no more nodes to explore

            bound = t  # increase threshold for next iteration
