# %% Import
from docplex.mp.model import Model
import tsplib95
import time
# %% Function to create distance matrix
def create_distance_matrix(file_path):
    problem = tsplib95.load(file_path)
    distance_matrix = {}
    for node1 in problem.get_nodes():
        for node2 in problem.get_nodes():
            if node1 != node2:
                distance_matrix[(node1, node2)] = problem.get_weight(node1, node2)
    return problem, distance_matrix
# %% Function to solve tsp
def solve_tsp(file_path):
    problem, distance_matrix = create_distance_matrix(file_path)
    #define model
    model = Model('TSP')

    #start time
    start_time = time.time()

    #define variables
    x_vars = {(i, j): model.binary_var(name=f'x_{i}_{j}') for i in problem.get_nodes() for j in problem.get_nodes() if i != j} #direct path from i to j
    u_vars = {i: model.integer_var(name=f'u_{i}', lb=1, ub=problem.dimension) for i in problem.get_nodes()}

    #define contraints
    for i in problem.get_nodes():
        model.add_constraint(model.sum(x_vars[i, j] for j in problem.get_nodes() if i != j) == 1)
        model.add_constraint(model.sum(x_vars[j, i] for j in problem.get_nodes() if i != j) == 1)

    #define mtz constraint
    M = problem.dimension
    for i in problem.get_nodes():
        for j in problem.get_nodes():
            if i != j and (i, j) in x_vars:
                model.add_constraint(u_vars[i] - u_vars[j] + M * x_vars[i, j] <= M - 1)
    
    #define objective function
    model.minimize(model.sum(distance_matrix[i, j] * x_vars[i, j] for i in problem.get_nodes() for j in problem.get_nodes() if i != j))

    #solve the problem
    solution = model.solve()

    #end time
    end_time = time.time()
    solve_time = end_time - start_time

    #print solution
    if solution:
        print("Solution found:")
        print(f"Total time = {solve_time}")
        for i in problem.get_nodes():
            for j in problem.get_nodes():
                if i != j and solution.get_value(x_vars[i, j]) > 0.5:
                    print(f"Route from {i} to {j}")
    else:
        print("No solution found.")

# %% Solve the problem
file_path = '/Users/hitwooo/Downloads/burma14.tsp'
print('test')
solve_tsp(file_path)