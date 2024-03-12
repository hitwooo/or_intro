# %% Import
from docplex.mp.model import Model
# %% Function for solve multiple knapsack problem
def solve_multiple_knapsack(items, knapsacks, profit, weights, capacities):
    n = len(items)
    m = len(knapsacks)
    
    # define model
    model = Model('MultipleKnapsack')

    # define variables
    x = model.binary_var_matrix(m, n, name = 'x')

    # add constraints
    for i in range(m):
        model.add_constraint(model.sum(weights[j] * x[i, j] for j in range(n)) <= capacities[i])    
    
    for j in range(n):
        model.add_constraint(model.sum(x[i,j] for i in range(m)) <= 1)

    # define objective function
    model.maximize(model.sum(profit[j]*x[i, j] for j in range(n) for i in range(m)))

    #solve the model
    solution = model.solve()

    if solution:
        print("Solution found:")
        for i in range(m):
            for j in range(n):
                if x[i, j].solution_value > 0.5: 
                    print(f"Item {j} is in knapsack {i}.")
    else:
        print("No solution found.")
