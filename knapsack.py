# %% Import
from docplex.mp.model import Model
import os
import pandas as pd
import time
# %% Function to extract data from file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n, wmax = map(int, lines[0].split())
        profits, weights = [],[]
        for line in lines[1:]:
            parts = line.split()
            if len(parts) != 2:
                continue
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

# %% 
results_df = pd.DataFrame(columns=['Instance name', 'number of items', 'knapsack capacity', 'Solution value', 'Solution status', 'Gap(%)', 'Time(sec)'])
# %% Function to solve knapsack problem
def solve_knapsack(n, wmax, profits, weights,results_df):
    model = Model(name='KnapsackProblem')
    start_time = time.time()
    x = model.binary_var_list(n, name='x')
    model.maximize(model.sum(x[i] * profits[i] for i in range(n)))
    model.add_constraint(model.sum(x[i] * weights[i] for i in range(n)) <= wmax)
    solution = model.solve()
    end_time = time.time()
    solve_time = end_time - start_time

    new_row = pd.DataFrame({
        'Instance name': [f'Problem {filename}'],
        'number of items': [n],
        'knapsack capacity': [wmax],
        'Solution value': [solution.get_objective_value() if solution else 'N/A'],
        'Solution status': [solution.solve_details.status if solution else 'No Solution Found'],
        'Time(sec)': [solve_time]
    })
    results_df = pd.concat([results_df, new_row], ignore_index=True)
    return results_df
# %% Low dimension
directory_path = '/Users/hitwooo/Desktop/OR/02 Coding/Knapsack/instances_01_KP/low-dimensional'
data_dict = process_files(directory_path)

for filename, data in data_dict.items():
    print(f'Solving knapsack problem for: {filename}')
    results_df = solve_knapsack(data['n'], data['wmax'], data['profits'], data['weights'],results_df)
# %% Large scale
directory_path = '/Users/hitwooo/Desktop/OR/02 Coding/Knapsack/instances_01_KP/large_scale_doable'
data_dict = process_files(directory_path)

for filename, data in data_dict.items():
    print(f'Solving knapsack problem for: {filename}')
    results_df = solve_knapsack(data['n'], data['wmax'], data['profits'], data['weights'],results_df)
# %%
excel_file_path = '/Users/hitwooo/Downloads/knapsack01_results.xlsx'
results_df.to_excel(excel_file_path, index=False, engine='openpyxl')