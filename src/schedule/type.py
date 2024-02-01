
from marshmallow import Schema, fields
from typing import List

from src.model.type import ScheduledTask

from ..model import BannedRange, Project, Task, ScheduledTask

from marshmallow import Schema, fields, validate, post_load
from typing import Literal, Optional
class TimeRangeSchema(Schema):
    timeRangeStart = fields.Float(required=True)
    timeRangeEnd = fields.Float(required=True)

class ScheduledTaskSchema(Schema):
    id = fields.Str(required=True)
    startTime = fields.Float(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return ScheduledTask(**data)

class TaskSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    projectId = fields.Str(required=True)
    priority = fields.Integer(validate=validate.OneOf([1, 2, 3, 4]), required=True)
    startTime = fields.Float(allow_none=True)
    duration = fields.Float(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)

class ProjectSchema(TimeRangeSchema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)

    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)

class BannedRangeSchema(TimeRangeSchema):
    id = fields.Str(required=True)

    @post_load
    def make_banned_range(self, data, **kwargs):
        return BannedRange(**data)
    

class ScheduleTasksRequestDTO:
    def __init__(
        self,
        tasks: List[Task], 
        projects: List[Project], 
        bannedRanges: List[BannedRange]
    ):
        self.tasks=tasks
        self.projects = projects
        self.bannedRanges = bannedRanges
        
    def __str__(self):
        return f"ScheduleTasksDTO(tasks={self.tasks}, projects={self.projects}, bannedRanges={self.bannedRanges})"
    
class ScheduleTasksRequestDTOSchema(Schema):
    tasks = fields.List(fields.Nested(TaskSchema), required=True)
    projects = fields.List(fields.Nested(ProjectSchema), required=True)
    bannedRanges = fields.List(fields.Nested(BannedRangeSchema), required=True)

    @post_load
    def make_schedule_tasks_request_dto(self, data, **kwargs):
        return ScheduleTasksRequestDTO(**data)
    
class ScheduleTasksResponseDTO:
    def __init__(
        self,
        scheduledTasks: List[ScheduledTask], 
        runId: str,
        score: float
    ):
        self.scheduledTasks=scheduledTasks
        self.runId = runId
        self.score = score
        
    def __str__(self):
        return f"ScheduleTasksDTO(scheduledTasks={self.scheduledTasks}, runId={self.runId}, score={self.score})"
    
class ScheduleTasksResponseDTOSchema(Schema):
    scheduledTasks = fields.List(fields.Nested(ScheduledTaskSchema), required=True)
    runId = fields.Str(required=True)
    score = fields.Float(required=False)

    @post_load
    def make_schedule_tasks_response_dto(self, data, **kwargs):
        return ScheduleTasksResponseDTO(**data)