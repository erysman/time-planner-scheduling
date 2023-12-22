import pulp
from model.constraints import addConstraints

from model.objective import setObjectiveFunction
from model.parameters import (
    getDecisionVariables,
    getModelParameters,
)
from model.type import Project, Task

from typing import List


def scheduleTasks(tasks: List[Task], projects: List[Project]):
    # TODO: skip tasks with startTime

    modelPrameters = getModelParameters(tasks, projects)
    decisionVariables = getDecisionVariables(modelPrameters.tasksIndicies)
    lp = pulp.LpProblem("tasksScheduleProblem", pulp.LpMaximize)
    setObjectiveFunction(lp, decisionVariables, modelPrameters)
    addConstraints(lp, decisionVariables, modelPrameters)
    lp.solve()

    for var in lp.variables():
        print(var, "=", pulp.value(var))

    print("OPT=", pulp.value(lp.objective))


# TODO: read startTimes from vars

# cplex jesli bedzie za wolno (mozna pobrać z ibm za darmo dla studentow)
# timeout w pulp
