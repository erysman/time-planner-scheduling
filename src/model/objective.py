import logging
import pulp
from .parameters import DecisionVariables, ModelParameters, TIME_NORMALIZATION_VALUE
import math


def buildObjectiveFunction(
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    tasksCount = len(modelPrameters.tasksIds)
    numberOfTasksWeight = max((3 * tasksCount - 6, 2))
    priorityOrderWeight = 1
    earlierStartsWeight = 0.25
    return (
        numberOfTasksWeight * maximizeNumberOfTasksWithHighPriority(decisionVariables, modelPrameters)
        - priorityOrderWeight * penalizeTasksNotOrderedByPriority(decisionVariables, modelPrameters)
        - earlierStartsWeight * penalizeLateStartTimes(decisionVariables, modelPrameters),
        "objective",
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

def penalizeTasksNotOrderedByPriority(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksPairs = modelPrameters.tasksPairs
    isIPriorityGreaterThanJ = modelPrameters.isIPriorityGreaterThanJ
    isIafterJ = decisionVariables.isIafterJ
    return pulp.lpSum(
        [isIafterJ[i][j] * isIPriorityGreaterThanJ[i][j] for i, j in tasksPairs]
    )

def penalizeLateStartTimes(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksIndicies = modelPrameters.tasksIndicies
    startTime = decisionVariables.startTime

    return (
        pulp.lpSum([(startTime[i]) for i in tasksIndicies])
        * TIME_NORMALIZATION_VALUE / 24
    )
