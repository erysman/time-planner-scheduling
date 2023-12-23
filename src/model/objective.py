import logging
import pulp
from .parameters import DecisionVariables, ModelParameters
import math


def setObjectiveFunction(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    tasksCount = len(modelPrameters.tasksIds)
    weight = max((3 * tasksCount - 6, 2))  # math.comb(tasksCount, 2)
    logging.info(f"using objective weight: {weight}")
    lp += (
        weight
        * maximizeNumberOfTasksWithHighPriority(decisionVariables, modelPrameters)
        + maximizeEarlierStartTimes(decisionVariables, modelPrameters)
        - penalizeTasksNotOrderedByPriority(decisionVariables, modelPrameters),
        "objective",
    )


def maximizeEarlierStartTimes(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksIndicies = modelPrameters.tasksIndicies
    startTime = decisionVariables.startTime

    return pulp.lpSum([(24-startTime[i]) for i in tasksIndicies])/24


def penalizeTasksNotOrderedByPriority(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksPairs = modelPrameters.tasksPairs
    isIPriorityGreaterThanJ = modelPrameters.isIPriorityGreaterThanJ
    isIafterJ = decisionVariables.isIafterJ
    return pulp.lpSum(
        [isIafterJ[i][j] * isIPriorityGreaterThanJ[i][j] for i, j in tasksPairs]
    )


def maximizeNumberOfTasksWithHighPriority(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksIndicies = modelPrameters.tasksIndicies
    priority = modelPrameters.priority
    priorityWeight = modelPrameters.priorityWeight
    isSheduled = decisionVariables.isSheduled

    return pulp.lpSum(
        [priorityWeight[priority[i]] * isSheduled[i] for i in tasksIndicies]
    )
