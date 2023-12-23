import logging
import pulp
import pprint
from .parameters import DecisionVariables, ModelParameters

pp = pprint.PrettyPrinter(indent=4)

def addConstraints(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    someStartTimesAreAlreadySet(lp, decisionVariables, modelPrameters)
    startTimesShouldNotExceedOneDay(lp, decisionVariables, modelPrameters)
    tasksShouldNotOverlapInTime(lp, decisionVariables, modelPrameters)
    tasksShouldNotExceedProjectTimeRange(lp, decisionVariables, modelPrameters)
    logging.debug(pp.pformat(lp.constraints))


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
        lp += (startTime[i] + duration[i] <= 24, f"endTime_less_then_24_{i}")


def tasksShouldNotOverlapInTime(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTime = decisionVariables.startTime
    isSheduled = decisionVariables.isSheduled
    isIafterJ = decisionVariables.isIafterJ

    for i, j in modelPrameters.tasksPairs:
        lp += (
            startTime[i] + modelPrameters.duration[i] * isSheduled[i]
            <= startTime[j] + 1000 * isIafterJ[i][j] + 1000 * (1 - isSheduled[j]),
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
        if initialStartTime[i] != None: continue
        lp += (
            startTime[i] >= projectTimeMin[i] * isSheduled[i],
            f"startTime_greater_than_projectTimeMin_{i}",
        )

    for i in modelPrameters.tasksIndicies:
        if initialStartTime[i] != None: continue
        lp += (
            startTime[i] + duration[i] <= projectTimeMax[i],
            f"endTime_less_than_projectTimeMax_{i}",
        )
