import logging
import pulp
from .parameters import DecisionVariables, ModelParameters, TIME_NORMALIZATION_VALUE
import math


def buildObjectiveFunction(
    dv: DecisionVariables,
    mp: ModelParameters,
):
    tasksCount = len(mp.tasksIds)
    w1 = max((3 * tasksCount - 6), 2)
    w2 = 1
    w3 = 0.25
    return (
        w1 * maximizeNumberOfTasks(dv, mp)
        - w2 * penalizeWrongOrder(dv, mp)
        - w3 * penalizeLateStartTimes(dv, mp),
        "objective",
    )

def maximizeNumberOfTasks(
    dv: DecisionVariables,
    mp: ModelParameters
):
    tasksIndicies = mp.tasksIndicies
    priority = mp.priority
    priorityWeight = mp.priorityWeight
    isSheduled = dv.isSheduled
    sum = []
    for i in tasksIndicies:
        sum.append(priorityWeight[priority[i]] * isSheduled[i])
    return pulp.lpSum(sum)


def penalizeWrongOrder(dv: DecisionVariables, mp: ModelParameters):
    tasksPairs = mp.tasksPairs
    isIPriorityGreaterThanJ = mp.isIPriorityGreaterThanJ
    isIafterJ = dv.isIafterJ
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
        * TIME_NORMALIZATION_VALUE
        / 24
    )
