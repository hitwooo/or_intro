# %% Import
from docplex.mp.model import Model
import tsplib95
# %% Function to create distance matrix
def create_distance_matrix(problem):
    distance_matrix = {}
    for node1 in problem.get_nodes():
        for node2 in problem.get_nodes():
            if node1 != node2:
                distance_matrix[(node1, node2)] = problem.get_weight(node1, node2)
    return distance_matrix
# %% Function to solve tsp
def solve_tsp(problem):
    distance_matrix = create_distance_matrix(problem)
    model = Model('TSP')
    x_vars = {(i, j): model.binary_var(name=f'x_{i}_{j}') for i in problem.get_nodes() for j in problem.get_nodes() if i != j}
    for i in problem.get_nodes():
        model.add_constraint(model.sum(x_vars[i, j] for j in problem.get_nodes() if i != j) == 1, f"leave_{i}")
        model.add_constraint(model.sum(x_vars[j, i] for j in problem.get_nodes() if i != j) == 1, f"enter_{i}")
    model.minimize(model.sum(distance_matrix[i, j] * x_vars[i, j] for i in problem.get_nodes() for j in problem.get_nodes() if i != j))
    solution = model.solve()
    if solution:
        print("Solution found:")
        for i in problem.get_nodes():
            for j in problem.get_nodes():
                if i != j and solution.get_value(x_vars[i, j]) > 0.5:
                    print(f"Route from {i} to {j}")
    else:
        print("No solution found.")
