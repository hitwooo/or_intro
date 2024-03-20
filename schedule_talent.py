#import
from docplex.mp.model import Model
import numpy as np
#function to solve problem
def solve_talent(data):
    n = len(data.columns) - 1
    d = data.iloc[-1]
    m = len(data.rows) -1
    # define model
    model = Model('TalentSchedule')

    # define variable
    x = model.binary_var_matrix(n,n,name = 'x')
    t = model.integer_var_list(n, name = 'start_scene')
    e = model.integer_var_list(m,name = 'earlier_shoot')
    l = model.integer_var_list(m,name = 'latest_shoot')
    z = model.binary_var_matrix(n,n,name = 'z')

    #define constraints
    model.add_constraint(model.sum(x[0,j] for j in range(n)) == 1)
    model.add_constraint(model.sum(x[k,n+1] for k in range(n)) == 1)
    for k in range(n):
        model.add_constraint(model.sum(x[k,j] for j in range(n) if j != k) == 1)
        model.add_constraint(model.sum(x[j,k] for j in range(n) if j != k) == 1)

    t[0] = 0
    t[n+1] = model.sum(d[i] for i in range(n) + 1)

    model.add_constraint(e[i] for i in range (m) <= t[j] for j in range(n))
    
    model.add_constraint()
    model.add_constraint()

    #define 
    solution = model.solve()

    return solution

# example



    
    
    
