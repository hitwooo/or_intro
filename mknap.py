# %%
from docplex.mp.model import Model
import re
# %% Functions for data extracting
def extract_data(block):
    one_line_data = ' '.join(block.split())
    parts = one_line_data.split()
    n, m, optimal_value = int(parts[0]), int(parts[1]), float(parts[2])
    p = [float(x) for x in parts[3:3+n]]
    constraint_data = [float(x) for x in parts[3+n:-m]]
    r = [constraint_data[i*n:(i+1)*n] for i in range(m)]
    b = [float(x) for x in parts[-m:]]
    return n, m, optimal_value, p, r, b

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
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

# %% Function to solve multidimensional knapsack problem
def solve_mknap(n,m,p,r,b):
    #define model
    model = Model('mknap')

    #define variables
    x = model.binary_var_list(n, name = 'x')
    #define constraints
    for i in range(m):
            model.add_constraint(model.sum(x[j] * r[i][j]  for j in range(n)) <= b[i])
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

#% file
file_path = '/Users/hitwooo/Downloads/mknap1.txt'
data_list = read_file(file_path)
#for data in data_list:
#    print(f"Solving multiple knapsack problem for: {data['problem_number']}")
#    solve_mknap(data['n'], data['m'], data['p'], data['r'], data['b'])

#print(data_list[0])
solve_mknap(data_list[0]['n'], data_list[0]['m'], data_list[0]['p'], data_list[0]['r'], data_list[0]['b'])

 
