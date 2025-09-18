from .solver import Solver
from sokoban.map import Map
from sokoban.moves import *
import heapq
import math
from sokoban.map import OBSTACLE_SYMBOL


class AStarSolver(Solver):
    """
    A* solver using Manhattan-distance heuristic for boxes.
    Chooses paths that minimize f(n) = g(n) + h(n),
    where g(n) is the number of moves so far, and h(n) is the estimated cost to goal.
    """

    def heuristic(self, state: Map) -> int:
        """
        Heuristic function: sum of minimum Manhattan distances
        from each box to the closest target.
        """
        # Deadlock detection: if any box (not on target) is in a static corner, return very high heuristic
        for (bx, by) in state.positions_of_boxes:
            if (bx, by) in state.targets:
                continue
            up = bx-1 < 0 or state.map[bx-1][by] == OBSTACLE_SYMBOL
            down = bx+1 >= state.length or state.map[bx+1][by] == OBSTACLE_SYMBOL
            left = by-1 < 0 or state.map[bx][by-1] == OBSTACLE_SYMBOL
            right = by+1 >= state.width or state.map[bx][by+1] == OBSTACLE_SYMBOL
            if (up and left) or (up and right) or (down and left) or (down and right):
                return 10**6
        total = 0
        for (bx, by) in state.positions_of_boxes:
            dmin = math.inf
            for (tx, ty) in state.targets:
                d = abs(bx - tx) + abs(by - ty)
                if d < dmin:
                    dmin = d
            total += dmin
        return total

    def solve(self) -> list[int] | None:
        """
        Runs A* search to find a solution.
        Returns a list of moves (as integers), or None if no solution is found.
        """
        start = self.map.copy()
        start_key = str(start)

        # Open list as a min-heap priority queue
        open_heap = []
        entry_count = 0  # tie-breaker counter to avoid comparing states directly

        # Push the initial state with f = h(start), g = 0
        heapq.heappush(open_heap, (self.heuristic(start), 0, entry_count, start, []))
        best_g = {start_key: 0}  # map state string -> best g(n)
        entry_count += 1

        while open_heap:
            f, g, _, state, path = heapq.heappop(open_heap)

            # Goal test
            if state.is_solved():
                return path

            # Expand current state
            for move in state.filter_possible_moves():
                nxt = state.copy()
                nxt.apply_move(move)
                new_g = g + 1
                key = str(nxt)

                # If this path is better than any previously found for this state
                if key not in best_g or new_g < best_g[key]:
                    best_g[key] = new_g
                    h = self.heuristic(nxt)
                    heapq.heappush(open_heap, (
                        new_g + h,  # f(n) = g(n) + h(n)
                        new_g,
                        entry_count,
                        nxt,
                        path + [move]
                    ))
                    entry_count += 1

        # No solution found
        return None