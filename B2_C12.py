# %% Import 
from docplex.mp.model import Model
import os

# %% Exercises 12.1 - 6
# Define the model
model1 = Model('MachineShop')

# Define integer variables
tow_bars = model1.integer_var(name = 'tow_bars')
stabilizer_bars = model1.integer_var(name = 'stabilizer_bars')

# Constants input
m1_maxhr = 16
m2_maxhr = 15
profit_tow = 130
profit_stabilizer = 150
tow_m1 = 3.2
stabilizer_m1 = 2.4
tow_m2 = 2
stabilizer_m2 = 3

# Constraints
model1.add_constraint(tow_m1*tow_bars+stabilizer_m1*stabilizer_bars <= m1_maxhr)
model1.add_constraint(tow_m2*tow_bars+stabilizer_m2*stabilizer_bars <= m2_maxhr)

# Objective function
model1.maximize(tow_bars*profit_tow + stabilizer_bars*profit_stabilizer)

# Solve the model
solution = model1.solve()

# Print the solution
if solution:
    print(f"Produce {solution[tow_bars]} tow bars")
    print(f"Produce {solution[stabilizer_bars]} stabilizer bars")
    print(f"Total profit will be ${solution.objective_value}")
else:
    print("No solution found")
# %% Exercises 12.3 - 1
# Define the model
model2 = Model('ProductMix')

# Define binary variables and production levels
x = model2.continuous_var_list(4, lb = 0, name = 'x')
y = model2.binary_var_list(4, name = 'y')
z = model2.binary_var(name = 'z')
# Constant input
start_up_costs = [50000, 40000, 70000, 60000]
marginal_revenue = [70, 60, 90, 80]
max_product = 2

#Constraints
model2.add_constraint(model2.sum(y[i] for i in range(4)) <= max_product)
model2.add_constraint(y[2] + y[3] <=2*(y[0] + y[1])) #not sure
model2.add_constraint(5*x[0] + 3*x[1] + 6*x[2] + 4*x[3] <= 6000 + 100000*z)
model2.add_constraint(4*x[0] + 6*x[1] + 3*x[2] + 5*x[3] <= 6000 + 100000*(1-z))

# Objective function
profit = model2.sum(marginal_revenue[i] * x[i] for i in range(4)) - model2.sum(start_up_costs[i] * y[i] for i in range(4))
model2.maximize(profit)

# Solve the model
solution = model2.solve()

# Print the solution
if solution:
    print("Optimal production levels:")
    for i in range(4):
        print(f"Product {i+1}: {solution[x[i]]} units")
    print(f"Total profit: {solution.get_objective_value()}")
else:
    print("No solution found")
# %% Exercises 12.3 - 5