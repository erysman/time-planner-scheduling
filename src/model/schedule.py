import logging
import pulp
from .constraints import addConstraints

from .objective import buildObjectiveFunction
from .parameters import (
    ModelParameters,
    buildDecisionVariables,
    buildModelParameters,
    TIME_NORMALIZATION_VALUE,
)
from .type import BannedRange, Project, ScheduledTask, Task, ScheduleResult
from typing import List

timeGranularity = 0.25  # 0.25 = 15 minutes
# SOLVER="GLPK_CMD"
# SOLVER = "PULP_CBC_CMD"
SOLVER = "CPLEX_CMD"
TIME_LIMIT_S = 10

# logging.basicConfig(level=logging.DEBUG)
print(pulp.listSolvers(onlyAvailable=True))


def scheduleTasks(
    tasks: List[Task],
    projects: List[Project],
    bannedRanges: List[BannedRange] = [],
    debug=False,
    timeLimit=TIME_LIMIT_S,
) -> ScheduleResult:
    modelPrameters = buildModelParameters(tasks, projects, bannedRanges)
    decisionVariables = buildDecisionVariables(
        modelPrameters.tasksIndicies, modelPrameters.bannedRangesIndicies
    )
    lp = pulp.LpProblem("tasksScheduleProblem", pulp.LpMaximize)
    lp += buildObjectiveFunction(decisionVariables, modelPrameters)
    addConstraints(lp, decisionVariables, modelPrameters)
    solver = pulp.getSolver(SOLVER, msg=0, timeLimit=timeLimit)
    status = lp.solve(solver)
    # if debug:
    logSolution(lp, status)
    score = pulp.value(lp.objective)
    scheduleTasks = buildSheduleTasksListFromSolvedModel(lp, modelPrameters, tasks, debug)
    return ScheduleResult(scheduleTasks, score)


def buildSheduleTasksListFromSolvedModel(
    lp: pulp.LpProblem, modelPrameters: ModelParameters, tasks: List[Task], debug=False
) -> List[ScheduledTask]:
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
            round(startTime * TIME_NORMALIZATION_VALUE / timeGranularity)
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
                round(startTime * TIME_NORMALIZATION_VALUE / 0.25) * 0.25
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


def logSolution(lp: pulp.LpProblem, status):
    for var in lp.variables():
        var_name = str(var)
        if "startTime" not in var_name and "isScheduled" not in var_name:
            continue
        logging.debug(f"{var_name} = {pulp.value(var)}")

    logging.debug(f"OPT = {pulp.value(lp.objective)}")
    logging.debug(f"status = {pulp.LpStatus[status]}")
