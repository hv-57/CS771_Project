from timing import timer
from abc import ABC, abstractmethod
from z3 import *

class NQueens_Framework(ABC):
	def __init__(self, n: int) -> None:
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

class Bool_Nqueens_Framework(NQueens_Framework):
	@timer('init_time')
	def __init__(self, n: int) -> None:
		super(Bool_Nqueens_Framework, self).__init__(n)

		self.queen_pos = [[Bool(f"Q_{i + 1}_{j + 1}") for j in range(n)] for i in range(n)]

		for i in range(n): 
			self.sol.add(PbEq([(x,1) for x in self.queen_pos[i]], 1))

		for j in range(n): 
			self.sol.add(PbEq([(self.queen_pos[i][j], 1) for i in range(n)], 1))

		for d in range(2 * n - 1):
			diagonal_vars = []
			for i in range(n):
				if 0 <= d - i < n:
					diagonal_vars.append(self.queen_pos[i][d - i])
			if len(diagonal_vars) > 1:
				self.sol.add(PbLe([(var, 1) for var in diagonal_vars], 1))

		for d in range(2 * n - 1):
			diagonal_vars = []
			for i in range(n):
				if 0 <= d - (n - 1 - i) < n:
					diagonal_vars.append(self.queen_pos[i][d - (n - 1 - i)])
			if len(diagonal_vars) > 1:
				self.sol.add(PbLe([(var, 1) for var in diagonal_vars], 1))

	@timer('invalidation_time')
	def invalidate_model(self, model: z3.ModelRef) -> None:
		self.sol.add(Or([Not(self.queen_pos[i][j]) if is_true(model.eval(self.queen_pos[i][j])) else self.queen_pos[i][j] for i in range(self.n) for j in range(self.n)]))

	def pretty_print(self, model: z3.ModelRef) -> None:
		for i in range(self.n):
			print(' '.join(['Q' if is_true(model.eval(self.queen_pos[i][j])) else '.' for j in range(self.n)]))
		print()

class Int_Nqueens_Framework(NQueens_Framework):
	@timer('init_time')
	def __init__(self, n: int) -> None:
		super(Int_Nqueens_Framework, self).__init__(n)

		self.queen_pos = [Int(f"Q_{i + 1}") for i in range(n)]
		
		for i in range(n):
			self.sol.add(And(1 <= self.queen_pos[i], self.queen_pos[i] <= n))
		
		self.sol.add(Distinct(self.queen_pos))
		
		for i in range(n):
			for j in range(i + 1, n):
				self.sol.add(Abs(self.queen_pos[i] - self.queen_pos[j]) != abs(i - j))
	
	@timer('invalidation_time')
	def invalidate_model(self, model: z3.ModelRef) -> None:
		self.sol.add(Or([self.queen_pos[i] != model.eval(self.queen_pos[i]) for i in range(self.n)]))

	def pretty_print(self, model: z3.ModelRef) -> None:
		for i in range(self.n):
			print(' '.join(['Q' if j == model.eval(self.queen_pos[i]).as_long() - 1 else '.' for j in range(self.n)]))
		print()

class BitVector_Nqueens_Framework(NQueens_Framework):
	@timer('init_time')
	def __init__(self, n: int) -> None:
		super(BitVector_Nqueens_Framework, self).__init__(n)

		self.queen_pos = [BitVec(f"Q_{i}", n) for i in range(n)]

		for i in range(n):
			self.sol.add(And([self.queen_pos[i] >= 0, self.queen_pos[i] < n]))

		for i in range(n):
			for j in range(i + 1, n):
				self.sol.add(self.queen_pos[i] != self.queen_pos[j])

		for i in range(n):
			for j in range(i + 1, n):
				self.sol.add(Abs(self.queen_pos[i] - self.queen_pos[j]) != abs(i - j))

	@timer('invalidation_time')
	def invalidate_model(self, model: z3.ModelRef) -> None:
		self.sol.add(Or([self.queen_pos[i] != model.eval(self.queen_pos[i]) for i in range(self.n)]))

	def pretty_print(self, model: z3.ModelRef) -> None:
		for i in range(self.n):
			print(' '.join(['Q' if j == model.eval(self.queen_pos[i]).as_long() else '.' for j in range(self.n)]))
		print()
