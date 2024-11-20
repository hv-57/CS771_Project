import argparse
from z3 import *
from solver import *

def solve_pigeonhole(m: int, n: int, framework: Type[Pigeonhole_Framework] = BitVector_Pigeonhole_Framework, init_time: bool = False, measure_all: bool = False, measure_individual: bool = False, display: bool = False, find_all: bool = False) -> tuple[bool, float]:
    solver = Pigeonhole_Solver(m, n, framework)

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

    if measure_all:
        print(f"Total time taken to find all solutions: {solver.total_time:.5f}s")

    if find_all:
        print(f"Total number of solutions: {solver.total_solutions}")

    return solver.total_solutions != 0, solver.total_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the Pigeonhole problem with optional timing.")
    parser.add_argument('m', type=int, help="Number of holes.")
    parser.add_argument('n', type=int, help="Number of pigeons.")
    parser.add_argument('framework', type=str, nargs='?', default='bit', choices=["bool", "int", "bit"], help="Framework to use")
    parser.add_argument('--display', action='store_true', help="Display the pigeonhole assignments.")
    parser.add_argument('--show-init-time', action='store_true', help="Show the time required for constraint initialization.")
    parser.add_argument('--find-all', action='store_true', help="Find all possible solutions.")
    parser.add_argument('--measure-all', action='store_true', help="Enable timing of the solver.")
    parser.add_argument('--measure-individual', action='store_true', help="Show time taken for calculating each individual solution.")

    args = parser.parse_args()

    frame_mapping = {'bool' : Bool_Pigeonhole_Framework, 'int' : Int_Pigeonhole_Framework, 'bit' : BitVector_Pigeonhole_Framework}

    solve_pigeonhole(
        m = args.m,
        n = args.n,
        framework = frame_mapping[args.framework],
        init_time = args.show_init_time,
        measure_all = args.measure_all or args.measure_individual,
        measure_individual = args.measure_individual,
        display = args.display,
        find_all = args.find_all
    )