import pulp
from .type import Project, Task
from .utils import generatePairs, generate2dArray
import math
from typing import Literal, List,TypedDict


class ModelParameters:
    def __init__(
        self,
        tasksIds: List[str],
        tasksIndicies: List[int],
        priority: List[Literal[1, 2, 3, 4]],
        priorityWeight: dict,
        duration: List[int],
        projectTimeMin: List[float],
        projectTimeMax: List[float],
        tasksPairs: List[tuple[int, int]],
        isIPriorityGreaterThanJ: List[List[int]],
        initialStartTime: List[float|None]
    ):
        self.tasksIds = tasksIds
        self.tasksIndicies = tasksIndicies
        self.priority = priority
        self.priorityWeight = priorityWeight
        self.duration = duration
        self.projectTimeMin = projectTimeMin
        self.projectTimeMax = projectTimeMax
        self.tasksPairs = tasksPairs
        self.isIPriorityGreaterThanJ = isIPriorityGreaterThanJ
        self.initialStartTime = initialStartTime

def calculatePriorityWeight(priority):
    return math.pow(2,priority)-1

def getModelParameters(tasks: List[Task], projects: List[Project]) -> ModelParameters:
    tasksIds = [task.id for task in tasks]
    tasksIndicies: List[int] = range(0, len(tasksIds))
    initialStartTime = [task.startTime for task in tasks]
    priority = [task.priority for task in tasks]
    maxPriority = max(priority)
    priorityWeight = {}
    for i in range(1, maxPriority+1):
        priorityWeight[i] = calculatePriorityWeight(i)
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
    tasksPairs = generatePairs(tasksIndicies)
    isIPriorityGreaterThanJ = generate2dArray(tasksIndicies)
    for i, j in tasksPairs:
        if priority[i] > priority[j]:
            isIPriorityGreaterThanJ[i][j] = 1
    return ModelParameters(
        tasksIds,
        tasksIndicies,
        priority,
        priorityWeight,
        duration,
        projectTimeMin,
        projectTimeMax,
        tasksPairs,
        isIPriorityGreaterThanJ,
        initialStartTime
    )


class DecisionVariables:
    def __init__(self, startTime: dict, isSheduled: dict, isIafterJ: dict):
        self.startTime = startTime
        self.isSheduled = isSheduled
        self.isIafterJ = isIafterJ


def getDecisionVariables(tasksIndicies: List[int]) -> DecisionVariables:
    startTime = pulp.LpVariable.dicts(
        "startTime", tasksIndicies, lowBound=0, upBound=24, cat="Continuous"
    )
    isSheduled = pulp.LpVariable.dicts(
        "isScheduled", tasksIndicies, lowBound=0, cat="Binary"
    )
    isIafterJ = pulp.LpVariable.dicts(
        "isIafterJ", (tasksIndicies, tasksIndicies), lowBound=0, cat="Binary"
    )
    return DecisionVariables(startTime, isSheduled, isIafterJ)
