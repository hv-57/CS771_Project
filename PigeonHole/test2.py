import matplotlib.pyplot as plt
from z3 import *
from pigeonhole import solve_pigeonhole

test_cases = [5, 10, 20, 50, 80]

m_values = [solve_pigeonhole(t, 20)[1] for t in test_cases]

plt.figure(figsize=(10, 6))
plt.plot(test_cases, m_values, marker='o', label="Time vs Number of Holes (m)")
plt.title("Time taken vs Number of Holes for n = 20")
plt.xlabel("Number of Holes (m)")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.legend()
plt.show()

n_values = [solve_pigeonhole(20, t)[1] for t in test_cases]

plt.figure(figsize=(10, 6))
plt.plot(test_cases, n_values, marker='o', label="Time vs Number of Pigeons (n)")
plt.title("Time taken vs Number of Pigeons for m = 20")
plt.xlabel("Number of Pigeons (n)")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.legend()
plt.show()
