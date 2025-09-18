from .solver import Solver
from sokoban.map import Map
from sokoban.moves import LEFT, RIGHT, UP, DOWN, BOX_LEFT, BOX_RIGHT, BOX_UP, BOX_DOWN
import math
from collections import deque


class PushIDAStarSolver(Solver):
    """
    Push-only IDA* solver.
    Operates on box-push moves using a heuristic based on the sum of Manhattan distances
    between boxes and their nearest targets. This ignores player movement and focuses on push actions.
    """

    def heuristic(self, state: Map) -> int:
        """
        Computes the sum of minimum Manhattan distances from each box
        to the closest target. Acts as an admissible and consistent heuristic.
        """
        total = 0
        for (bx, by) in state.positions_of_boxes:
            dmin = math.inf
            for (tx, ty) in state.targets:
                d = abs(bx - tx) + abs(by - ty)
                if d < dmin:
                    dmin = d
            total += dmin
        return total

    def find_pushes(self, state: Map):
        """
        Finds all legal push actions the player can perform from the current state.

        Returns:
            List of move codes (BOX_LEFT, BOX_RIGHT, etc.) representing valid pushes.
        """
        # Compute all reachable positions for the player (ignoring boxes)
        reachable = set()
        dq = deque([(state.player.x, state.player.y)])
        reachable.add((state.player.x, state.player.y))

        while dq:
            x, y = dq.popleft()
            for move, dx, dy in [(LEFT, 0, -1), (RIGHT, 0, 1), (UP, 1, 0), (DOWN, -1, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < state.length and
                    0 <= ny < state.width and
                    state.map[nx][ny] != 1 and
                    (nx, ny) not in state.positions_of_boxes and
                    (nx, ny) not in reachable
                ):
                    reachable.add((nx, ny))
                    dq.append((nx, ny))

        pushes = []
        # For each box, check if it can be pushed from a reachable position
        for (bx, by) in state.positions_of_boxes:
            for move, dx, dy, code in [
                (LEFT, 0, -1, BOX_LEFT),
                (RIGHT, 0, 1, BOX_RIGHT),
                (UP, 1, 0, BOX_UP),
                (DOWN, -1, 0, BOX_DOWN)
            ]:
                px, py = bx - dx, by - dy  # required player position
                tx, ty = bx + dx, by + dy  # target box position after push
                if (
                    (px, py) in reachable and
                    0 <= tx < state.length and
                    0 <= ty < state.width and
                    state.map[tx][ty] != 1 and
                    (tx, ty) not in state.positions_of_boxes
                ):
                    pushes.append(code)

        return pushes

    def solve(self) -> list[int] | None:
        """
        Entry point for the Push-IDA* solver.
        Returns a list of box-push move codes that solve the puzzle,
        or None if no solution is found.
        """
        start = self.map.copy()
        bound = self.heuristic(start)

        # Iterative deepening: reset visited and path each iteration
        while True:
            visited = set()
            visited.add((tuple(sorted(start.positions_of_boxes.keys())), (start.player.x, start.player.y)))
            path = []

            def search(state: Map, g: int, bound: int) -> tuple[int, list[int] | None]:
                """
                Recursive bounded-depth search using heuristic pruning.

                Returns:
                    - (cost, path) if goal is found
                    - (new bound, None) if current path exceeds threshold
                """
                f = g + self.heuristic(state)
                if f > bound:
                    return f, None
                if state.is_solved():
                    return f, path.copy()

                min_next = math.inf
                push_list = self.find_pushes(state)

                for code in push_list:
                    nxt = state.copy()
                    try:
                        nxt.apply_move(code)
                    except ValueError:
                        continue  # illegal move, skip

                    key = (
                        tuple(sorted(nxt.positions_of_boxes.keys())),
                        (nxt.player.x, nxt.player.y)
                    )

                    if key in visited:
                        continue

                    visited.add(key)
                    path.append(code)

                    t, result = search(nxt, g + 1, bound)

                    if result is not None:
                        return t, result

                    if t < min_next:
                        min_next = t

                    path.pop()
                    visited.remove(key)

                return min_next, None

            # Depth-first search within current bound
            t, result = search(start, 0, bound)
            if result is not None:
                return result
            if t == math.inf:
                return None
            bound = t

