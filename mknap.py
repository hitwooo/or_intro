# %%
from docplex.mp.model import Model
# %% Function to solve multidimensional knapsack problem
def solve_mknap(n,m,p,r,b):
    #define model
    model = Model('mknap')

    #define variables
    x = model.binary_var_list(n, name = 'x')

    #define constraints
    for i in range(m):
        model.add_constraint(model.sum(x[j] * r[i][j] for j in range(n)) <= b[i])
    #define objective function
    model.maximize(model.sum(p[j] * x[j] for j in range(n)))

    #solve model
    solution = model.solve()

    if solution:
        print("Solution found:")
        print(f"Optimal value: {solution.get_objective_value()}")
        for j in range(n):
            if x[j].solution_value > 0.5:
                print(f"Item {j} is selected.")
    else:
        print("No solution found.")
# %% test
n = 6
m = 10
p = [100, 600, 1200, 2400, 500, 2000]
r = [[8, 12, 13, 64, 22, 41],
     [8, 12, 13, 75, 22, 41],
     [3, 6, 4, 18, 6, 4],
     [5, 10, 8, 32, 6, 12],
     [5, 13, 8, 42, 6, 20],
     [5, 13, 8, 48, 6, 20],
     [0, 0, 0, 0, 8, 0],
     [3, 0, 4, 0, 8, 0],
     [3, 2, 4, 0, 8, 4],
     [3, 2, 4, 8, 8, 4]]
b = [80, 96, 20, 36, 44, 48, 10, 18, 22, 24]
solve_mknap(n, m, p, r, b)
