import sys
import time
from sokoban import Box, DOWN, Map, Player
from sokoban.moves import moves_meaning
from search_methods.ida_star import IDAStarSolver
from search_methods.simulated_annealing import SimulatedAnnealingSolver
from search_methods.a_star import AStarSolver
from search_methods.push_a_star import PushAStarSolver
from search_methods.push_idastar import PushIDAStarSolver


if __name__ == '__main__':
    # Parse command-line arguments
    if len(sys.argv) >= 3:
        alg_arg = sys.argv[1].lower()
        map_path = sys.argv[2]
    elif len(sys.argv) == 2:
        alg_arg = None
        map_path = sys.argv[1]
    else:
        alg_arg = None
        map_path = 'tests/easy_map2.yaml'

    print(f"Loading map from: {map_path}")
    crt_map = Map.from_yaml(map_path)
    print("\nInitial Map:")
    print(crt_map)

    # Choose solver
    if alg_arg in ('ida*', 'ida', 'ida-star', 'ida_star'):
        solver = IDAStarSolver(crt_map)
        alg_name = "IDA*"
    elif alg_arg in ('simulated-annealing', 'simanneal', 'annealing'):
        solver = SimulatedAnnealingSolver(crt_map)
        alg_name = "Simulated Annealing"
    elif alg_arg is None:
        if 'easy' in map_path:
            solver = IDAStarSolver(crt_map)
            alg_name = "IDA*"
        elif 'medium' in map_path:
            solver = AStarSolver(crt_map)
            alg_name = "A*"
        elif 'hard' in map_path:
            solver = PushIDAStarSolver(crt_map)
            alg_name = "Push-IDA*"
        elif 'large' in map_path or 'super_hard' in map_path:
            solver = AStarSolver(crt_map)
            alg_name = "A*"
        else:
            solver = IDAStarSolver(crt_map)
            alg_name = "IDA*"
    else:
        print(f"Unknown algorithm: {alg_arg}")
        sys.exit(1)

    # Run solver with timing
    print(f"\nRunning {alg_name} solver...")
    start_time = time.time()
    try:
        moves = solver.solve()
    except KeyboardInterrupt:
        print("Search interrupted. Falling back to Simulated Annealing.")
        solver = SimulatedAnnealingSolver(crt_map)
        moves = solver.solve()
        alg_name = "Simulated Annealing (fallback)"
    elapsed_time = time.time() - start_time

    if moves is None:
        print("No solution found with Push-IDA*. Falling back to A*.")
        solver = AStarSolver(crt_map)
        alg_name = "A* (fallback)"
        start_time = time.time()
        moves = solver.solve()
        elapsed_time = time.time() - start_time
        if moves is None:
            print("No solution found with A* either.")
            sys.exit(1)

    # Output solution
    print(f"\nAlgorithm used: {alg_name}")
    print(f"Execution time: {elapsed_time:.2f} seconds")
    print(f"Number of moves: {len(moves)}")
    print("Solution moves:", [moves_meaning[m] for m in moves])

    # Apply and display final state
    final = crt_map.copy()
    for m in moves:
        final.apply_move(m)

    print("\nFinal Map:")
    print(final)

    if final.is_solved():
        print("\nSolved!")
    else:
        print("\nNot solved.")
