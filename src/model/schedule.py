import logging
import pulp
from .constraints import addConstraints

from .objective import setObjectiveFunction
from .parameters import (
    ModelParameters,
    getDecisionVariables,
    getModelParameters,
    timeNormalizationValue
)
from .type import BannedRange, Project, Task
from typing import List

logging.basicConfig(level=logging.DEBUG)

def scheduleTasks(tasks: List[Task], projects: List[Project], bannedRanges: List[BannedRange]=[]) -> List[Task]:
    # print(pulp.listSolvers(onlyAvailable=True))
    modelPrameters = getModelParameters(tasks, projects, bannedRanges)
    decisionVariables = getDecisionVariables(modelPrameters.tasksIndicies, modelPrameters.bannedRangesIndicies)
    lp = pulp.LpProblem("tasksScheduleProblem", pulp.LpMaximize)
    setObjectiveFunction(lp, decisionVariables, modelPrameters)
    addConstraints(lp, decisionVariables, modelPrameters)
    solver = pulp.getSolver("GLPK_CMD", msg=0, timeLimit=5) #5
    lp.solve(solver)
    logSolution(lp)
    return buildTasksListFromSolvedModel(lp, modelPrameters, tasks)


def buildTasksListFromSolvedModel(
    lp: pulp.LpProblem, modelPrameters: ModelParameters, tasks: List[Task]
) -> List[Task]:
    solvedVariables = lp.variablesDict()
    resultTasks = []
    for i in modelPrameters.tasksIndicies:
        isScheduled = pulp.value(solvedVariables[f"isScheduled_{i}"])
        startTime = pulp.value(solvedVariables[f"startTime_{i}"])
        taskId = modelPrameters.tasksIds[i]
        task = [task for task in tasks if task.id == taskId][0]
        resultTask = Task(
            taskId,
            task.name,
            task.projectId,
            task.priority,
            round(startTime*timeNormalizationValue/0.25)*0.25 if isScheduled else None,
            task.duration,
        )
        resultTasks.append(resultTask)
    
    sortedTasks = sorted(resultTasks, key=lambda t: (t.startTime is None, t.startTime))
    for t in sortedTasks:
        logging.debug(t)
    return sortedTasks


# cplex jesli bedzie za wolno (mozna pobrać z ibm za darmo dla studentow)
# timeout w pulp


def logSolution(lp: pulp.LpProblem):
    for var in lp.variables():
        logging.debug(f"{var} = {pulp.value(var)}")

    logging.debug(f"OPT = {pulp.value(lp.objective)}")
