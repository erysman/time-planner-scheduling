import logging
import pulp
from .parameters import DecisionVariables, ModelParameters, TIME_NORMALIZATION_VALUE

BIG_M = 1000

def addConstraints(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    someStartTimesAreAlreadySet(lp, decisionVariables, modelPrameters)
    startTimesShouldNotExceedOneDay(lp, decisionVariables, modelPrameters)
    tasksShouldNotOverlapInTime(lp, decisionVariables, modelPrameters)
    tasksShouldNotExceedProjectTimeRange(lp, decisionVariables, modelPrameters)
    tasksShouldNotOverlapWithBannedRanges(lp, decisionVariables, modelPrameters)

def someStartTimesAreAlreadySet(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTime = decisionVariables.startTime
    isSheduled = decisionVariables.isSheduled
    initialStartTime = modelPrameters.initialStartTime
    for i in modelPrameters.tasksIndicies:
        if initialStartTime[i] != None:
            startTime[i].setInitialValue(initialStartTime[i])
            startTime[i].fixValue()
            isSheduled[i].setInitialValue(1)
            isSheduled[i].fixValue()
            logging.debug(f"task {i} startTime fixed to {initialStartTime[i]}")


def startTimesShouldNotExceedOneDay(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTime = decisionVariables.startTime
    duration = modelPrameters.duration

    for i in modelPrameters.tasksIndicies:
        lp += (startTime[i] >= 0, f"startTime_greater_than_0_{i}")

    for i in modelPrameters.tasksIndicies:
        lp += (
            startTime[i] + duration[i] <= 24 / TIME_NORMALIZATION_VALUE,
            f"endTime_less_then_24_{i}",
        )


def tasksShouldNotOverlapInTime(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTime = decisionVariables.startTime
    isSheduled = decisionVariables.isSheduled
    isIafterJ = decisionVariables.isIafterJ
    initialStartTime = modelPrameters.initialStartTime

    for i, j in modelPrameters.tasksPairs:
        if initialStartTime[i] != None and initialStartTime[j] != None:
            continue
        lp += (
            startTime[i] + modelPrameters.duration[i] * isSheduled[i]
            <= startTime[j] + BIG_M * isIafterJ[i][j] + BIG_M * (1 - isSheduled[j]),
            f"tasks_{i}_{j}_cant_overlap",
        )
        lp += (isIafterJ[i][j] + isIafterJ[j][i] <= 1, f"tasks_{i}_{j}_cant_overlap2")
        lp += (isIafterJ[i][j] <= isSheduled[i], f"tasks_{i}_{j}_cant_overlap3")
        lp += (isIafterJ[i][j] <= isSheduled[j], f"tasks_{i}_{j}_cant_overlap4")


def tasksShouldNotExceedProjectTimeRange(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTime = decisionVariables.startTime
    isSheduled = decisionVariables.isSheduled
    duration = modelPrameters.duration
    projectTimeMax = modelPrameters.projectTimeMax
    projectTimeMin = modelPrameters.projectTimeMin
    initialStartTime = modelPrameters.initialStartTime

    for i in modelPrameters.tasksIndicies:
        if initialStartTime[i] != None:
            continue
        lp += (
            startTime[i] >= projectTimeMin[i] * isSheduled[i],
            f"startTime_greater_than_projectTimeMin_{i}",
        )

    for i in modelPrameters.tasksIndicies:
        if initialStartTime[i] != None:
            continue
        lp += (
            startTime[i] + duration[i] <= projectTimeMax[i],
            f"endTime_less_than_projectTimeMax_{i}",
        )

def tasksShouldNotOverlapWithBannedRanges(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    initialStartTime = modelPrameters.initialStartTime
    startTime = decisionVariables.startTime
    isSheduled = decisionVariables.isSheduled
    isTaskIafterRangeA = decisionVariables.isTaskIafterRangeA
    duration = modelPrameters.duration
    bannedRangeStartTime = modelPrameters.bannedRangeStartTime
    bannedRangeEndTime = modelPrameters.bannedRangeEndTime
    for i in modelPrameters.tasksIndicies:
        if initialStartTime[i] != None:
            continue;
        for k in modelPrameters.bannedRangesIndicies:
            lp += (
                startTime[i] + duration[i] * isSheduled[i]
                <= bannedRangeStartTime[k] + BIG_M * (isTaskIafterRangeA[i][k]),
                f"task{i}_endTime_less_than_bannedRange{k}_startTime",
            )
            lp += (
                startTime[i] + BIG_M * (1 - isSheduled[i])
                >= bannedRangeEndTime[k] * (isTaskIafterRangeA[i][k]),
                f"task{i}_startTime_greater_than_bannedRange{k}_endTime",
            )
