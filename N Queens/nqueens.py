import argparse
from z3 import *
from solver import *

def solve_n_queens(n: int, framework: Type[NQueens_Framework] = Bool_Nqueens_Framework, init_time: bool = False, measure_all: bool = False, measure_individual: bool = False, display: bool = True, find_all: bool = False) -> None:
    solver = NQueens_Solver(n, framework)

    if init_time:
        print(f"Time taken to initialize constraints: {solver.init_time:.5f}s")

    while True:
        found, time = solver.gen_next()
        if not found:
            break
        if measure_individual:
            print(f"Time taken to find solution: {time:.5f} seconds")
        if display:
            solver.pretty_print()
        if not find_all:
            break

    if solver.total_solutions == 0:
        print("No solutions found.")

    if measure_all:
        print(f"Total time taken to find all solutions: {solver.total_time:.5f}s")

    if find_all:
        print(f"Total number of solutions: {solver.total_solutions}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the N-Queens problem with optional timing.")
    parser.add_argument('n', type=int, help="Size of the chess board (n x n).")
    parser.add_argument('framework', type=str, nargs='?', default='bool', choices=["bool", "int", "bit"], help="Framework to use")
    parser.add_argument('--display', action='store_true', help="Display the chessboard for each solution.")
    parser.add_argument('--show-init-time', action='store_true', help="Show the time required for constraint initialization.")
    parser.add_argument('--find-all', action='store_true', help="Find all possible solutions.")
    parser.add_argument('--measure-all', action='store_true', help="Enable timing of the solver.")
    parser.add_argument('--measure-individual', action='store_true', help="Show time taken for calculating each individual solution.")

    args = parser.parse_args()

    frame_mapping = {'bool' : Bool_Nqueens_Framework, 'int' : Int_Nqueens_Framework, 'bit' : BitVector_Nqueens_Framework}

    solve_n_queens(
        n = args.n, 
        framework = frame_mapping[args.framework],
        init_time = args.show_init_time, 
        measure_all = args.measure_all or args.measure_individual, 
        measure_individual = args.measure_individual, 
        display = args.display, 
        find_all = args.find_all
    )