import pulp
from model.type import Project, Task
from model.utils import generatePairs, generate2dArray


from typing import Literal, List


class ModelParameters:
    def __init__(
        self,
        tasksIndicies: List[int],
        priority: List[Literal[1, 2, 3, 4]],
        duration: List[int],
        projectTimeMin: List[float],
        projectTimeMax: List[float],
        tasksPairs: List[tuple[int, int]],
        isIPriorityGreaterThanJ: List[List[int]],
    ):
        self.tasksIndicies = tasksIndicies
        self.priority = priority
        self.duration = duration
        self.projectTimeMin = projectTimeMin
        self.projectTimeMax = projectTimeMax
        self.tasksPairs = tasksPairs
        self.isIPriorityGreaterThanJ = isIPriorityGreaterThanJ


def getModelParameters(tasks: List[Task], projects: List[Project]) -> ModelParameters:
    tasksIds = [task.id for task in tasks]
    tasksIndicies: List[int] = range(0, len(tasksIds))
    priority = [task.priority for task in tasks]
    duration = [task.duration for task in tasks]
    projectTimeMin = [
        next(
            project.timeRangeStart
            for project in projects
            if project.id == task.projectId
        )
        for task in tasks
    ]
    projectTimeMax = [
        next(
            project.timeRangeEnd for project in projects if project.id == task.projectId
        )
        for task in tasks
    ]
    print(projectTimeMin, projectTimeMax)

    tasksPairs = generatePairs(tasksIndicies)
    isIPriorityGreaterThanJ = generate2dArray(tasksIndicies)
    for i, j in tasksPairs:
        if priority[i] > priority[j]:
            isIPriorityGreaterThanJ[i][j] = 1
    return ModelParameters(
        tasksIndicies,
        priority,
        duration,
        projectTimeMin,
        projectTimeMax,
        tasksPairs,
        isIPriorityGreaterThanJ,
    )


class DecisionVariables:
    def __init__(self, startTime: dict, isSheduled: dict, isIafterJ: dict):
        self.startTime = startTime
        self.isSheduled = isSheduled
        self.isIafterJ = isIafterJ


def getDecisionVariables(tasksIndicies: List[int]) -> DecisionVariables:
    startTime = pulp.LpVariable.dicts(
        "startTimeVar", tasksIndicies, lowBound=0, upBound=24, cat="Continuous"
    )
    isSheduled = pulp.LpVariable.dicts(
        "scheduledVar", tasksIndicies, lowBound=0, cat="Binary"
    )
    isIafterJ = pulp.LpVariable.dicts(
        "isIafterJVar", (tasksIndicies, tasksIndicies), lowBound=0, cat="Binary"
    )
    return DecisionVariables(startTime, isSheduled, isIafterJ)
