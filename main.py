import logging
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from src.schedule.scheduleRoute import scheduleBlueprint
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.register_blueprint(scheduleBlueprint)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8082)))