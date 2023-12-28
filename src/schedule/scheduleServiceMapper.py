import logging
from src.schedule.type import ScheduleTasksRequestDTOSchema, ScheduleTasksResponseDTO, ScheduleTasksResponseDTOSchema


class ScheduleServiceMapper:
    _instance = None

    def __new__(cls, requestSchema: ScheduleTasksRequestDTOSchema, responseSchema: ScheduleTasksResponseDTOSchema):
        if cls._instance is None:
            cls._instance = super(ScheduleServiceMapper, cls).__new__(cls)
            # Initialization code here
            cls.requestSchema = requestSchema
            cls.responseSchema = responseSchema
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        logging.debug("DeserializerService singleton initialized")

    def deserialize(self, json: str):
        dto = self.requestSchema.loads(json)
        return dto
    
    def serialize(self, object: ScheduleTasksResponseDTO):
        dto = self.responseSchema.dumps(object)
        return dto
        