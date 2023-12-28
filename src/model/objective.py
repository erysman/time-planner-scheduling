import logging
import pulp
from .parameters import DecisionVariables, ModelParameters, timeNormalizationValue
import math


def setObjectiveFunction(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    tasksCount = len(modelPrameters.tasksIds)
    numberOfTasksWeight = max((3 * tasksCount - 6, 2))  # math.comb(tasksCount, 2)
    logging.info(f"using objective numberOfTasksWeight: {numberOfTasksWeight}")
    earlierStartsWeight = 0.25
    lp += (
        numberOfTasksWeight * maximizeNumberOfTasksWithHighPriority(decisionVariables, modelPrameters)
        + penalizeTasksNotOrderedByPriority(decisionVariables, modelPrameters)
        + earlierStartsWeight * penalizeLateStartTimes(decisionVariables, modelPrameters),
        "objective",
    )


def penalizeLateStartTimes(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksIndicies = modelPrameters.tasksIndicies
    startTime = decisionVariables.startTime

    return (
        pulp.lpSum([(-startTime[i]) for i in tasksIndicies])
        * timeNormalizationValue
        / 24
    )


def penalizeTasksNotOrderedByPriority(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksPairs = modelPrameters.tasksPairs
    isIPriorityGreaterThanJ = modelPrameters.isIPriorityGreaterThanJ
    isIafterJ = decisionVariables.isIafterJ
    return -pulp.lpSum(
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
