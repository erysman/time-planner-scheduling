import pulp
from model.constraints import addConstraints

from model.objective import setObjectiveFunction
from model.parameters import (
    ModelParameters,
    getDecisionVariables,
    getModelParameters,
)
from model.type import Project, Task

from typing import List


def scheduleTasks(tasks: List[Task], projects: List[Project]) -> List[Task]:
    modelPrameters = getModelParameters(tasks, projects)
    decisionVariables = getDecisionVariables(modelPrameters.tasksIndicies)
    lp = pulp.LpProblem("tasksScheduleProblem", pulp.LpMaximize)
    setObjectiveFunction(lp, decisionVariables, modelPrameters)
    addConstraints(lp, decisionVariables, modelPrameters)
    lp.solve()
    return buildTasksListFromSolvedModel(lp, modelPrameters, tasks)
    
def buildTasksListFromSolvedModel(lp: pulp.LpProblem, modelPrameters: ModelParameters, tasks: List[Task]) -> List[Task]:
    solvedVariables = lp.variablesDict()
    resultTasks = []
    for i in modelPrameters.tasksIndicies:
        isScheduled = pulp.value(solvedVariables[f"isScheduled_{i}"])
        startTime = pulp.value(solvedVariables[f"startTime_{i}"])
        taskId = modelPrameters.tasksIds[i]
        task = [task for task in tasks if task.id == taskId][0]
        resultTask = Task(taskId, task.name, task.projectId, task.priority, startTime if isScheduled else None, task.duration)
        print(resultTask)
        resultTasks.append(resultTask)
    # TODO append tasks, that were skipped because already had a startTime 
    return resultTasks


# cplex jesli bedzie za wolno (mozna pobrać z ibm za darmo dla studentow)
# timeout w pulp
