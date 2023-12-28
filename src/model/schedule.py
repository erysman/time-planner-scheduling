import logging
import pulp
from .constraints import addConstraints

from .objective import setObjectiveFunction
from .parameters import (
    ModelParameters,
    getDecisionVariables,
    getModelParameters,
    timeNormalizationValue,
)
from .type import BannedRange, Project, ScheduledTask, Task
from typing import List

timeGranularity = 0.25  # 0.25 = 15 minutes

# logging.basicConfig(level=logging.DEBUG)


def scheduleTasks(
    tasks: List[Task],
    projects: List[Project],
    bannedRanges: List[BannedRange] = [],
    debug=False,
) -> List[Task]:
    # print(pulp.listSolvers(onlyAvailable=True))
    modelPrameters = getModelParameters(tasks, projects, bannedRanges)
    decisionVariables = getDecisionVariables(
        modelPrameters.tasksIndicies, modelPrameters.bannedRangesIndicies
    )
    lp = pulp.LpProblem("tasksScheduleProblem", pulp.LpMaximize)
    setObjectiveFunction(lp, decisionVariables, modelPrameters)
    addConstraints(lp, decisionVariables, modelPrameters)
    solver = pulp.getSolver("GLPK_CMD", msg=0, timeLimit=5)  # 5
    lp.solve(solver)
    logSolution(lp)
    return buildTasksListFromSolvedModel(lp, modelPrameters, tasks, debug)


def buildTasksListFromSolvedModel(
    lp: pulp.LpProblem, modelPrameters: ModelParameters, tasks: List[Task], debug=False
) -> List[Task]:
    solvedVariables = lp.variablesDict()
    allTasks = []
    scheduledTasks = []
    for i in modelPrameters.tasksIndicies:
        isScheduled = pulp.value(solvedVariables[f"isScheduled_{i}"])
        if not isScheduled:
            continue
        startTime = pulp.value(solvedVariables[f"startTime_{i}"])
        taskId = modelPrameters.tasksIds[i]
        if startTime == None:
            raise Exception(f"Task {taskId} is scheduled, but doesn't have startTime!")
        resultTask = ScheduledTask(
            taskId,
            round(startTime * timeNormalizationValue / timeGranularity)
            * timeGranularity,
        )
        scheduledTasks.append(resultTask)
        if debug:
            task = [task for task in tasks if task.id == taskId][0]
            resultTask = Task(
                task.id,
                task.name,
                task.projectId,
                task.priority,
                round(startTime * timeNormalizationValue / 0.25) * 0.25
                if isScheduled
                else None,
                task.duration,
            )
            allTasks.append(resultTask)
    if debug:
        sortedTasks = sorted(allTasks, key=lambda t: (t.startTime is None, t.startTime))
        for t in sortedTasks:
            logging.debug(t)
    sortedScheduledTasks = sorted(
        scheduledTasks, key=lambda t: (t.startTime is None, t.startTime)
    )
    return sortedScheduledTasks


def logSolution(lp: pulp.LpProblem):
    for var in lp.variables():
        logging.debug(f"{var} = {pulp.value(var)}")

    logging.debug(f"OPT = {pulp.value(lp.objective)}")
