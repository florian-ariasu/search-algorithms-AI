from .solver import Solver
from sokoban.map import Map, OBSTACLE_SYMBOL, TARGET_SYMBOL
from sokoban.moves import LEFT, RIGHT, UP, DOWN, BOX_LEFT, BOX_RIGHT, BOX_UP, BOX_DOWN
import heapq
import math
from collections import deque

try:
    from munkres import Munkres
    MUNKRES_AVAILABLE = True
except ImportError:
    MUNKRES_AVAILABLE = False

class PushAStarSolver(Solver):
    """
    A* solver over box-pushes: each action is pushing a box, player moves are computed implicitly.
    """
    def heuristic(self, state: Map) -> int:
        if MUNKRES_AVAILABLE:
            # optimal assignment of boxes to targets
            boxes = list(state.positions_of_boxes.keys())
            targets = list(state.targets)
            matrix = [[abs(bx-tx) + abs(by-ty) for tx,ty in targets] for bx,by in boxes]
            m = Munkres()
            cost = 0
            for r, c in m.compute(matrix):
                cost += matrix[r][c]
            return cost
        # fallback: sum of minimal Manhattan distances
        total = 0
        for (bx, by) in state.positions_of_boxes:
            dmin = math.inf
            for (tx, ty) in state.targets:
                d = abs(bx - tx) + abs(by - ty)
                if d < dmin:
                    dmin = d
            total += dmin
        return total

    def is_deadlock(self, state: Map) -> bool:
        # simple corner deadlock: any non-target box in a static corner
        for (bx, by) in state.positions_of_boxes:
            if (bx, by) in state.targets:
                continue
            up = bx-1 < 0 or state.map[bx-1][by] == OBSTACLE_SYMBOL
            down = bx+1 >= state.length or state.map[bx+1][by] == OBSTACLE_SYMBOL
            left = by-1 < 0 or state.map[bx][by-1] == OBSTACLE_SYMBOL
            right = by+1 >= state.width or state.map[bx][by+1] == OBSTACLE_SYMBOL
            # corner
            if (up and left) or (up and right) or (down and left) or (down and right):
                return True
            # freeze deadlock: two boxes along a wall with obstacles on one side
            # horizontal pair
            if (bx, by+1) in state.positions_of_boxes:
                # obstacles above both
                if (bx-1 < 0 or (state.map[bx-1][by] == OBSTACLE_SYMBOL and state.map[bx-1][by+1] == OBSTACLE_SYMBOL)):
                    return True
                # obstacles below both
                if (bx+1 >= state.length or (state.map[bx+1][by] == OBSTACLE_SYMBOL and state.map[bx+1][by+1] == OBSTACLE_SYMBOL)):
                    return True
            # vertical pair
            if (bx+1, by) in state.positions_of_boxes:
                # obstacles left of both
                if (by-1 < 0 or (state.map[bx][by-1] == OBSTACLE_SYMBOL and state.map[bx+1][by-1] == OBSTACLE_SYMBOL)):
                    return True
                # obstacles right of both
                if (by+1 >= state.width or (state.map[bx][by+1] == OBSTACLE_SYMBOL and state.map[bx+1][by+1] == OBSTACLE_SYMBOL)):
                    return True
        return False

    def solve(self) -> list[int] | None:
        start = self.map.copy()
        start_key = (tuple(sorted(start.positions_of_boxes.keys())), (start.player.x, start.player.y))
        open_heap = []
        heapq.heappush(open_heap, (self.heuristic(start), 0, start, []))
        best_g = {start_key: 0}

        while open_heap:
            f, g, state, path = heapq.heappop(open_heap)
            if state.is_solved():
                return path
            # compute reachable cells for player ignoring boxes
            reachable = set()
            dq = deque()
            dq.append((state.player.x, state.player.y))
            reachable.add((state.player.x, state.player.y))
            while dq:
                x, y = dq.popleft()
                for move, dx, dy in [(LEFT,0,-1),(RIGHT,0,1),(UP,1,0),(DOWN,-1,0)]:
                    nx, ny = x + dx, y + dy
                    # bounds & obstacle & box check
                    if 0 <= nx < state.length and 0 <= ny < state.width:
                        if state.map[nx][ny] != 1 and (nx,ny) not in state.positions_of_boxes:
                            if (nx,ny) not in reachable:
                                reachable.add((nx,ny))
                                dq.append((nx,ny))
            # for each box, try push in each direction
            for (bx, by), box_name in state.positions_of_boxes.items():
                for dir, dx, dy, box_move in [
                    (LEFT, 0,-1, BOX_LEFT),
                    (RIGHT,0,1, BOX_RIGHT),
                    (UP, 1,0, BOX_UP),
                    (DOWN,-1,0, BOX_DOWN)
                ]:
                    # target cell for push
                    tx, ty = bx + dx, by + dy
                    # player must stand opposite side
                    px, py = bx - dx, by - dy
                    if (px,py) in reachable and 0 <= tx < state.length and 0 <= ty < state.width:
                        # skip validity check: rely on apply_move catching invalid pushes
                        # generate next state
                        nxt = state.copy()
                        try:
                            nxt.apply_move(box_move)
                        except ValueError:
                            continue
                        # prune simple corner deadlocks
                        if self.is_deadlock(nxt):
                            continue
                        new_g = g + 1
                        key = (tuple(sorted(nxt.positions_of_boxes.keys())), (nxt.player.x, nxt.player.y))
                        if key not in best_g or new_g < best_g[key]:
                            best_g[key] = new_g
                            h = self.heuristic(nxt)
                            heapq.heappush(open_heap, (new_g + h, new_g, nxt, path + [box_move]))
        return None

