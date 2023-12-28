# scheduleRoute.py
import logging
from flask import Blueprint, jsonify, g, request

from .type import ScheduleTasksRequestDTOSchema, ScheduleTasksResponseDTOSchema
from .scheduleService import ScheduleService
from .scheduleServiceMapper import ScheduleServiceMapper

version = 'v1'
path = 'scheduleTasks'
scheduleBlueprint = Blueprint('schedule', __name__)

def scheduleServicesRequired(f):
    def decorated_function(*args, **kwargs):
        g.scheduleService = ScheduleService()
        g.scheduleMapperService = ScheduleServiceMapper(ScheduleTasksRequestDTOSchema(), ScheduleTasksResponseDTOSchema())
        return f(*args, **kwargs)
    return decorated_function

@scheduleBlueprint.post(f"/{version}/{path}")
@scheduleServicesRequired
def scheduleTasks():
    if request.is_json:
        jsonBody = request.get_data(as_text=True)
        logging.debug(jsonBody)
        try:
            dto = g.scheduleMapperService.deserialize(jsonBody)
            response = g.scheduleService.schedule(dto)
            responseJson = g.scheduleMapperService.serialize(response)
            logging.debug(responseJson)
            return responseJson, 200, {'Content-type': 'application/json'}
        except Exception as e:
            logging.error(e)
            return {"error": f"Error: {e}"}, 400
    return {"error": "Request must be JSON"}, 415