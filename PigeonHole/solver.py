from z3 import *
from frameworks import *
from timing import benchmark
from typing import Type

class Pigeonhole_Solver:
	def __init__(self, m: int, n: int, framework: Type[Pigeonhole_Framework]) -> None:
		self.m = m;
		self.n = n
		self.framework = framework(m, n)
		self.total_solutions = 0
		self.total_time = 0
		self.init_time = benchmark['init_time']

	def gen_next(self) -> tuple[bool, float]:
		res, self.cur_model = self.framework.solve()
		cur_time = benchmark['solve_time']
		self.total_time += benchmark['solve_time']

		if res == unsat:
			return False, cur_time

		self.total_solutions += 1
		self.framework.invalidate_model(self.cur_model)

		self.total_time += benchmark['invalidation_time']

		return True, cur_time
	
	def pretty_print(self) -> None:
		self.framework.pretty_print(self.cur_model)