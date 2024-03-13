# %%
from docplex.mp.model import Model
import re
import pandas as pd
import time 
# %% Functions for data extracting
# Extract data within block
def extract_data(block):
    one_line_data = ' '.join(block.split())
    parts = one_line_data.split()
    n, m, optimal_value = int(parts[0]), int(parts[1]), float(parts[2])
    p = [float(x) for x in parts[3:3+n]]
    constraint_data = [float(x) for x in parts[3+n:-m]]
    r = [constraint_data[i*n:(i+1)*n] for i in range(m)]
    b = [float(x) for x in parts[-m:]]
    return n, m, optimal_value, p, r, b

# Extract data from the file path
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    #extract blocks
    blocks = re.split(r'\n\s*\n+', content.strip())
    data_list = []  
    for index, block in enumerate(blocks[1:]):
        n, m, optimal_value, p, r, b = extract_data(block)  
        data_list.append({
            'problem_number': index + 1, 
            'n': n,
            'm': m,
            'optimal_value': optimal_value,
            'p': p,
            'r': r,
            'b': b        
        })
    return data_list
# %%
results_df = pd.DataFrame(columns=['Instance name', 'Knapsacks', 'Objects', 'Solution value', 'Optimal Value', 'Solution status', 'Gap(%)', 'Time(sec)'])
# %% Function to solve multidimensional knapsack problem
def solve_mknap(problem_number,n,m,optimal_value,p,r,b,results_df):
    #define model
    model = Model('mknap')
    
    #start time
    start_time = time.time()

    #define variables
    x = model.binary_var_list(n, name = 'x')

    #define constraints
    for i in range(m):
            model.add_constraint(model.sum(x[j] * r[i][j]  for j in range(n)) <= b[i])
    #define objective function
    model.maximize(model.sum(p[j] * x[j] for j in range(n)))

    #solve model
    solution = model.solve()

    #end time
    end_time = time.time()
    solve_time = end_time - start_time

    #data frame to store value
    new_row = pd.DataFrame({
        'Instance name': [f'Problem {problem_number}'],
        'Knapsacks': [m],
        'Objects': [n],
        'Solution value': [solution.get_objective_value() if solution else 'N/A'],
        'Optimal Value': [optimal_value],
        'Solution status': [solution.solve_details.status if solution else 'No Solution Found'],
        'Gap(%)': [((solution.get_objective_value() - optimal_value) / solution.get_objective_value()) * 100 if solution.get_objective_value() != 0 else 'N/A'],
        'Time(sec)': [solve_time]
    })
    results_df = pd.concat([results_df, new_row], ignore_index=True)
    return results_df

#% Test instances
file_path = '/Users/hitwooo/Downloads/mknap1.txt'
data_list = read_file(file_path)
for data in data_list:
    results_df = solve_mknap(data['problem_number'],data['n'], data['m'],data['optimal_value'], data['p'], data['r'], data['b'],results_df)


excel_file_path = '/Users/hitwooo/Downloads/mknap_results.xlsx'
results_df.to_excel(excel_file_path, index=False, engine='openpyxl')