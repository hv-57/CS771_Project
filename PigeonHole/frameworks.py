from timing import timer
from abc import ABC, abstractmethod
from z3 import *

class Pigeonhole_Framework(ABC):
    def __init__(self, m: int, n: int) -> None:
        self.m = m
        self.n = n
        self.sol = Solver()

    @abstractmethod
    def invalidate_model(self, model: z3.ModelRef) -> None:
        pass

    @abstractmethod
    def pretty_print(self, model: z3.ModelRef) -> None:
        pass

    @timer('solve_time')
    def solve(self) -> tuple[CheckSatResult, z3.ModelRef | None]:
        res = self.sol.check()
        if res == sat:
            return res, self.sol.model()
        else:
            return res, None


class Bool_Pigeonhole_Framework(Pigeonhole_Framework):
    @timer('init_time')
    def __init__(self, m: int, n: int) -> None:
        super(Bool_Pigeonhole_Framework, self).__init__(m, n)

        self.pigeonhole_pos = [[Bool(f"P_{i+1}_{j+1}") for j in range(m)] for i in range(n)]

        for i in range(n):
            self.sol.add(PbEq([(x, 1) for x in self.pigeonhole_pos[i]], 1))

        for j in range(m):
            self.sol.add(PbLe([(self.pigeonhole_pos[i][j], 1) for i in range(n)], 1))

    @timer('invalidation_time')
    def invalidate_model(self, model: z3.ModelRef) -> None:
        self.sol.add(Or([Not(self.pigeonhole_pos[i][j]) if is_true(model.eval(self.pigeonhole_pos[i][j])) else self.pigeonhole_pos[i][j] for i in range(self.n) for j in range(self.m)]))

    def pretty_print(self, model: z3.ModelRef) -> None:
        for i in range(self.n):
            print(f"Pigeon {i + 1}: " + ' '.join(['H' if is_true(model.eval(self.pigeonhole_pos[i][j])) else '.' for j in range(self.m)]))
        print()


class Int_Pigeonhole_Framework(Pigeonhole_Framework):
    @timer('init_time')
    def __init__(self, m: int, n: int) -> None:
        super(Int_Pigeonhole_Framework, self).__init__(m, n)

        self.pigeonhole_pos = [Int(f"P_{i+1}") for i in range(n)]

        for i in range(n):
            self.sol.add(And(1 <= self.pigeonhole_pos[i], self.pigeonhole_pos[i] <= m))

        self.sol.add(Distinct(self.pigeonhole_pos))

    @timer('invalidation_time')
    def invalidate_model(self, model: z3.ModelRef) -> None:
        self.sol.add(Or([self.pigeonhole_pos[i] != model.eval(self.pigeonhole_pos[i]) for i in range(self.n)]))

    def pretty_print(self, model: z3.ModelRef) -> None:
        for i in range(self.n):
            print(f"Pigeon {i + 1}: Hole {model.eval(self.pigeonhole_pos[i]).as_long()}")
        print()

class BitVector_Pigeonhole_Framework(Pigeonhole_Framework):
    @timer('init_time')
    def __init__(self, m: int, n: int) -> None:
        super(BitVector_Pigeonhole_Framework, self).__init__(m, n)

        self.pigeonhole_pos = [BitVec(f"P_{i}", m) for i in range(n)]

        for pigeon in self.pigeonhole_pos:
            self.sol.add(And([pigeon >= 0, pigeon < m]))
        
        for i in range(n):
            for j in range(i + 1, n):
                self.sol.add(self.pigeonhole_pos[i] != self.pigeonhole_pos[j])

    @timer('invalidation_time')
    def invalidate_model(self, model: z3.ModelRef) -> None:
        self.sol.add(Or([self.pigeonhole_pos[i] != model.eval(self.pigeonhole_pos[i]) for i in range(self.n)]))

    def pretty_print(self, model: z3.ModelRef) -> None:
        for i in range(self.n):
            print(f"Pigeon {i + 1}: Hole {model.eval(self.pigeonhole_pos[i]).as_long() + 1}")
        print()
