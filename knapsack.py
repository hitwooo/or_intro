# %% Import library
from docplex.mp.model import Model
import os
import pandas as pd
import time

# %% Create a class
class knapsack01_solver:
    def __init__(self):
        self.results_df = pd.DataFrame(columns=['Instance name', 'Number of items', 'Knapsack capacity', 'Solution value', 'Solution status', 'Gap(%)', 'Time(sec)'])
    
    # function to read instances
    def read_file(self, file_path):
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

    # function to read files from directory
    def process_files(self, directory_path):
        data_dict = {}
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                n, wmax, profits, weights = self.read_file(file_path)
                data_dict[filename] = {
                    'n': n,
                    'wmax': wmax,
                    'profits': profits,
                    'weights': weights
                }
        return data_dict

    # function to solve the knapsack problem
    def solve_knapsack(self, n, wmax, profits, weights,filename):

        # define model
        model = Model(name='KnapsackProblem')

        # set timer
        start_time = time.time()

        # define variable
        x = model.binary_var_list(n, name='x')

        # define objective function
        model.maximize(model.sum(x[i] * profits[i] for i in range(n)))

        # define constraint
        model.add_constraint(model.sum(x[i] * weights[i] for i in range(n)) <= wmax)

        # solve the problem
        solution = model.solve()

        # end timer
        end_time = time.time()
        solve_time = end_time - start_time

        # add results to new row
        new_row = pd.DataFrame({
            'Instance name': [f'Problem {filename}'],
            'Number of items': [n],
            'Knapsack capacity': [wmax],
            'Solution value': [solution.get_objective_value() if solution else 'N/A'],
            'Solution status': [solution.solve_details.status if solution else 'No Solution Found'],
            'Time(sec)': [solve_time]
        })
        self.results_df = pd.concat([self.results_df, new_row], ignore_index=True)
        return self.results_df
    
    # function to solve from directory path
    def solve_all(self, directory_path):
        data_dict = self.process_files(directory_path)
        for filename, data in data_dict.items():
            print(f'Solving knapsack problem for: {filename}')
            self.solve_knapsack(data['n'], data['wmax'], data['profits'], data['weights'], filename)
        print(self.results_df)

# Example
solver = knapsack01_solver()
low_dim_path = '/Users/hitwooo/Desktop/OR/02 Coding/Knapsack/instances_01_KP/low-dimensional'
solver.solve_all(low_dim_path)