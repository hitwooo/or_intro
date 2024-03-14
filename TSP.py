# %% Import
from docplex.mp.model import Model
import tsplib95
import time
import matplotlib.pyplot as plt
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
    u_vars = {i: model.integer_var(name=f'u_{i}', lb=1, ub=model.infinity) for i in problem.get_nodes()}

    #define contraints
    for i in problem.get_nodes():
        model.add_constraint(model.sum(x_vars[i, j] for j in problem.get_nodes() if i != j) == 1)
        model.add_constraint(model.sum(x_vars[j, i] for j in problem.get_nodes() if i != j) == 1)

    #define mtz constraint
    M = problem.dimension
    for i in range(M):
        for j in range(M):
            if i != j and (i, j) in x_vars:
                model.add_constraint(u_vars[i] - u_vars[j] + M * x_vars[i, j] <= M - 1)
    
    #define objective function
    model.minimize(model.sum(distance_matrix[i, j] * x_vars[i, j] for i in problem.get_nodes() for j in problem.get_nodes() if i != j))

    #solve the problem
    solution = model.solve()

    #end time
    end_time = time.time()
    solve_time = end_time - start_time

    return problem, solution, x_vars, solve_time
# %% Function to plot geo data
def plot_tour_geo(file_path):
    problem, solution, x_vars,solve_time = solve_tsp(file_path)
    print(solve_time)
    geo_points = {node: problem.node_coords[node] for node in problem.get_nodes()}
    
    for node in problem.get_nodes():
        plt.plot(geo_points[node][1], geo_points[node][0], 'bo')  # Plot long as x, lat as y

    for i, j in x_vars.keys():
        if solution.get_value(x_vars[i, j]) > 0.5:
            plt.plot([geo_points[i][1], geo_points[j][1]], [geo_points[i][0], geo_points[j][0]], 'g-')

    # Additional plot settings
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('TSP Solution on GEO Coordinates')
    plt.grid(True)
    plt.show()

# %% Solve the problem
file_path = '/Users/hitwooo/Downloads/gr96.tsp'
plot_tour_geo(file_path)
