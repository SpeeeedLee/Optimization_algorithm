from pulp import LpProblem, LpVariable, LpMaximize
from pulp import LpStatus


# Just a simple funciton for printing out the solution given by "pulp" library
def print_result(model):
    print(f"model status : {LpStatus[model.status]}")
    print(f"objective value : {model.objective.value()}")

    for var in model.variables():
        print(f"{var.name} : {var.value()}")

# Calculate how much tons ONE UNIT of A, B, C, D are
T1 = 100 / (1500*0.05+500*0.1+1000*0.05+100*0.8)
T2 = 150 / (1500*0.05+500*0.15+1000*0.1+100*0.7)
T3 = 200 / (1500*0.1+500*0.2+1000*0.1+100*0.6)
T4 = 250 / (1500*0.15+500*0.05+1000*0.15+100*0.65)

# 實例化一個instance, 其名字為model。
# sense 是要說明這是找最大值還最小值的問題
model = LpProblem(name = 'Profit Maximization Problem', sense = LpMaximize)

# Define Decision Variables (即解空間中的變數們)
A = LpVariable(name = 'A', lowBound = 5000)
B = LpVariable(name = 'B', lowBound = 0)
C = LpVariable(name = 'C', lowBound = 0)
D = LpVariable(name = 'D', lowBound = 4000)

# Add some constraints to the model
model.addConstraint( A*T1*0.05 + B*T2*0.05 + C*T3*0.1 + D*T4*0.15 <= 1000, 'Nitrates Constraint')
model.addConstraint( A*T1*0.1 + B*T2*0.15 + C*T3*0.2 + D*T4*0.05 <= 2000, 'Phosphates Constraint')
model.addConstraint( A*T1*0.05 + B*T2*0.1 + C*T3*0.1 + D*T4*0.15 <= 1500, 'Potash Constraint')

# Set the Objective Function
model.setObjective((350-100)*A + (550-150)*B + (450-200)*C + (700-250)*D)

# Just a single line to solbe the defined LP model
model.solve()


print_result(model)

'''
model status : Optimal
objective value : 12595429.975
A : 9048.3871
B : 21333.333
C : 0.0
D : 4000.0
'''