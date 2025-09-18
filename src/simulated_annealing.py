from .solver import Solver
from sokoban.map import Map
from sokoban.moves import *
import random
import math


class SimulatedAnnealingSolver(Solver):
    """
    Simulated Annealing solver:
    Uses a probabilistic approach to explore the state space,
    accepting worse states with decreasing probability to escape local minima.
    """

    def solve(
        self,
        initial_temp: float = 5000.0,
        cooling_rate: float = 0.9999,
        min_temp: float = 1e-6,
        max_iter: int = 100000,
        restarts: int = 20
    ) -> list[int] | None:

        initial_map = self.map.copy()
        overall_best_cost = math.inf
        overall_best_path: list[int] = []

        # Heuristic cost function: total Manhattan distance from boxes to nearest targets
        def cost(state: Map) -> float:
            total = 0
            for (bx, by) in state.positions_of_boxes:
                dmin = math.inf
                for (tx, ty) in state.targets:
                    d = abs(bx - tx) + abs(by - ty)
                    if d < dmin:
                        dmin = d
                total += dmin
                # Penalize boxes not yet on target
                if (bx, by) not in state.targets:
                    total += 10
            return total

        # Try multiple random restarts to avoid getting stuck in poor regions
        for attempt in range(restarts):
            current = initial_map.copy()
            best = current.copy()
            path: list[int] = []
            best_path: list[int] = []
            curr_cost = cost(current)
            best_cost = curr_cost
            T = initial_temp  # initial temperature

            # Iterative improvement with temperature-based acceptance
            for i in range(max_iter):
                # Early termination if solution is found
                if curr_cost == 0 or current.is_solved():
                    return path

                # Generate neighbors
                moves_list = current.filter_possible_moves()
                if not moves_list:
                    break

                mv = random.choice(moves_list)
                nxt = current.copy()
                nxt.apply_move(mv)
                new_cost = cost(nxt)
                delta = new_cost - curr_cost

                # Accept new state based on energy delta or probability
                if delta < 0 or random.random() < math.exp(-delta / T):
                    current = nxt
                    path.append(mv)
                    curr_cost = new_cost

                    # Update best state found in this restart
                    if new_cost < best_cost:
                        best = current.copy()
                        best_cost = new_cost
                        best_path = path.copy()

                # Decrease temperature
                T *= cooling_rate
                if T < min_temp:
                    break

            # Update best state across all restarts
            if best_cost < overall_best_cost:
                overall_best_cost = best_cost
                overall_best_path = best_path

            # Early exit if solution found during restarts
            if overall_best_cost == 0:
                return overall_best_path

        # Return best path found across all restarts, if any
        if overall_best_cost == 0:
            return overall_best_path
        return None
