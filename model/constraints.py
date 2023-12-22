import pulp
import pprint
from model.parameters import DecisionVariables, ModelParameters


def addConstraints(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    startTimesShouldNotExceedOneDay(lp, decisionVariables, modelPrameters)
    tasksShouldNotOverlapInTime(lp, decisionVariables, modelPrameters)
    tasksShouldNotExceedProjectTimeRange(lp, decisionVariables, modelPrameters)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lp.constraints)


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

    for i in modelPrameters.tasksIndicies:
        lp += (
            startTime[i] >= projectTimeMin[i] * isSheduled[i],
            f"startTime_greater_than_projectTimeMin_{i}",
        )

    for i in modelPrameters.tasksIndicies:
        lp += (
            startTime[i] + duration[i] <= projectTimeMax[i],
            f"endTime_less_than_projectTimeMax_{i}",
        )
