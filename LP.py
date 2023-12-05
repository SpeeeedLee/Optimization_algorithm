'''
This is an example for how to use python  package to solve Linear Programming Problem

Refernece: https://www.learnwithshin.com/post/%E6%89%BE%E5%87%BA%E6%9C%80%E4%BD%B3%E8%A7%A3-linear-programming
'''

from pulp import LpProblem, LpVariable, LpMaximize
from pulp import LpStatus


# 實例化一個instance, 其名字為model。
# sense 是要說明這是找最大值還最小值的問題
model = LpProblem(name = 'example', sense = LpMaximize)


# Define Decision Variables (及解空間中的變數們)
toy = LpVariable(name = 'toy', lowBound = 0)
book = LpVariable(name = 'book', lowBound = 0) #(也有upBound可以用)

# Add some constraints to the model
model.addConstraint(toy <= 50, 'constraint_1')
model.addConstraint(book + toy <= 120, 'constraint_2')

# Set the Objective Function
model.setObjective(toy*2 + book)

# Just a single line to solbe the defined LP model
model.solve()

# The status
'''
{0 : "Not Solved",
1 : "Optimal"
-1 : "Infeasible"
-2 : "Unbounded"
-3 : "Undefined"}
'''

# To see the results
'''
print(model.objective.value())
print(book.value())
print(toy.value())
'''

# Create a simple funciton to see the result
def print_result(model):
    print(f"model status : {LpStatus[model.status]}")
    print(f"objective value : {model.objective.value()}")

    for var in model.variables():
        print(f"{var.name} : {var.value()}")


print_result(model)