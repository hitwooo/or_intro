# %% Import
from docplex.mp.model import Model
import os

# %% Function to extract data from file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n, wmax = map(int, lines[0].split())
        profits, weights = [],[]
        for line in lines[1:]:
            v, w = map(float, line.split())
            profits.append(v)
            weights.append(w)
    return n, wmax, profits, weights

# %% Import files from directory
def process_files(directory_path):
    data_dict = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path,filename)
            n, wmax, profits, weights = read_file(file_path)
            data_dict[filename] = {
                'n': n,
                'wmax' : wmax,
                'profits': profits,
                'weights': weights        
            }
    return data_dict

# %% Function to solve knapsack problem
def solve_knapsack(n, wmax, profits, weights):
    model = Model(name='KnapsackProblem')
    x = model.binary_var_list(n, name='x')
    model.maximize(model.sum(x[i] * profits[i] for i in range(n)))
    model.add_constraint(model.sum(x[i] * weights[i] for i in range(n)) <= wmax)
    solution = model.solve()
    
    if solution:
        print('The solution to the problem is:')
        for i in range(n):
            if solution.get_value(x[i]) > 0.5:
                print(f'Item {i}: Profit = {profits[i]}, Weight = {weights[i]}')
        print(f'Total profit: {solution.objective_value}')
    else:
        print('No solution found')
# %%
directory_path = '/Users/hitwooo/Desktop/OR/02 Coding/Knapsack/instances_01_KP/low-dimensional'
data_dict = process_files(directory_path)

for filename, data in data_dict.items():
    print(f'Solving knapsack problem for: {filename}')
    solve_knapsack(data['n'], data['wmax'], data['profits'], data['weights'])
# %%
