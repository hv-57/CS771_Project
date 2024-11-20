from nqueens import solve_n_queens

test_values = [4, 6, 8, 16]

for n in test_values:
	print(f"Testing for n = {n}:")
	solve_n_queens(n, display=True)

