import pulp
from model.parameters import DecisionVariables, ModelParameters


def setObjectiveFunction(
    lp: pulp.LpProblem,
    decisionVariables: DecisionVariables,
    modelPrameters: ModelParameters,
):
    lp += (
        maximizeNumberOfTasksWithHighPriority(decisionVariables, modelPrameters)
        - penalizeTasksNotOrderedByPriority(decisionVariables, modelPrameters),
        "objective",
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


def maximizeNumberOfTasksWithHighPriority(
    decisionVariables: DecisionVariables, modelPrameters: ModelParameters
):
    tasksIndicies = modelPrameters.tasksIndicies
    priority = modelPrameters.priority
    isSheduled = decisionVariables.isSheduled
    return pulp.lpSum([priority[i] * isSheduled[i] for i in tasksIndicies])
