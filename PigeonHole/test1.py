from pigeonhole import solve_pigeonhole

test_cases = [(10, 10), (10, 15), (15, 15)]

for m, n in test_cases:
	print(solve_pigeonhole(m, n)[0])