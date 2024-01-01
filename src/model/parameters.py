import logging
import pulp
from .type import BannedRange, Project, Task
from .utils import generatePairs, generate2dArray
import math
from typing import Literal, List, TypedDict

# if timeNormalizationValue=24, all time values are normalized to range 0-1 from 0-24 (when timeNormalizationValue=1)
timeNormalizationValue = 1
maxPriority = 4


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
        initialStartTime: List[float | None],
        bannedRangesIndicies: List[int],
        bannedRangeStartTime: List[float],
        bannedRangeEndTime: List[float],
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
        self.bannedRangesIndicies = bannedRangesIndicies
        self.bannedRangeStartTime = bannedRangeStartTime
        self.bannedRangeEndTime = bannedRangeEndTime


def calculatePriorityWeight(priority):
    return math.pow(2, priority) - 1


def getModelParameters(
    tasks: List[Task], projects: List[Project], bannedRanges: List[BannedRange]
) -> ModelParameters:
    tasksIds = [task.id for task in tasks]
    tasksIndicies: List[int] = range(0, len(tasksIds))
    initialStartTime = buildInitialStartTimeParameter(tasks)
    priority = [task.priority for task in tasks]
    priorityWeight = buildPriorityWeights(maxPriority)
    duration = [task.duration / timeNormalizationValue for task in tasks]
    projectTimeMin = buildProjectTimeMinList(tasks, projects)
    projectTimeMax = buildProjectTimeMaxList(tasks, projects)
    tasksPairs = generatePairs(tasksIndicies)
    isIPriorityGreaterThanJ = buildPriorityRelationshipMatrix(
        tasksIndicies, priority, tasksPairs
    )

    bannedRangesIds = [range.id for range in bannedRanges]
    bannedRangesIndicies: List[int] = range(0, len(bannedRangesIds))
    bannedRangeStartTime = [range.timeRangeStart for range in bannedRanges]
    bannedRangeEndTime = [range.timeRangeEnd for range in bannedRanges]
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
        initialStartTime,
        bannedRangesIndicies,
        bannedRangeStartTime,
        bannedRangeEndTime,
    )

def buildInitialStartTimeParameter(tasks):
    return [
        (
            task.startTime / timeNormalizationValue
            if task.startTime != None
            else task.startTime
        )
        for task in tasks
    ]


def buildPriorityRelationshipMatrix(tasksIndicies, priority, tasksPairs):
    isIPriorityGreaterThanJ = generate2dArray(tasksIndicies)
    for i, j in tasksPairs:
        if priority[i] > priority[j]:
            isIPriorityGreaterThanJ[i][j] = 1
    return isIPriorityGreaterThanJ


def buildProjectTimeMaxList(tasks, projects):
    return [
        next(
            project.timeRangeEnd / timeNormalizationValue
            for project in projects
            if project.id == task.projectId
        )
        for task in tasks
    ]


def buildProjectTimeMinList(tasks, projects):
    return [
        next(
            project.timeRangeStart / timeNormalizationValue
            for project in projects
            if project.id == task.projectId
        )
        for task in tasks
    ]

def buildPriorityWeights(maxPriority):
    priorityWeight = {}
    for i in range(1, maxPriority + 1):
        priorityWeight[i] = calculatePriorityWeight(i)
    return priorityWeight


class DecisionVariables:
    def __init__(self, startTime: dict, isSheduled: dict, isIafterJ: dict, isTaskIafterRangeA: dict):
        self.startTime = startTime
        self.isSheduled = isSheduled
        self.isIafterJ = isIafterJ
        self.isTaskIafterRangeA = isTaskIafterRangeA


def getDecisionVariables(tasksIndicies: List[int], bannedRangesIndicies: List[int]) -> DecisionVariables:
    startTime = pulp.LpVariable.dicts(
        "startTime",
        tasksIndicies,
        lowBound=0,
        upBound=24 / timeNormalizationValue,
        cat="Continuous",
    )
    isSheduled = pulp.LpVariable.dicts(
        "isScheduled", tasksIndicies, lowBound=0, cat="Binary"
    )
    isIafterJ = pulp.LpVariable.dicts(
        "isIafterJ", (tasksIndicies, tasksIndicies), lowBound=0, cat="Binary"
    )
    isTaskIafterRangeA = pulp.LpVariable.dicts(
        "isTaskIafterRangeA", (tasksIndicies, bannedRangesIndicies), lowBound=0, cat="Binary"
    )
    return DecisionVariables(startTime, isSheduled, isIafterJ, isTaskIafterRangeA)
