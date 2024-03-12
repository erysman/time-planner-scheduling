
# Time-planner-scheduling server

## Deploy

```bash

docker build -t time-planner-scheduling .
docker image tag time-planner-scheduling europe-central2-docker.pkg.dev/time-planner-dc611/time-planner-server/scheduling
docker image push europe-central2-docker.pkg.dev/time-planner-dc611/time-planner-server/scheduling
```

## Run

### Run container

`docker run --rm -it -p 8082:8082 time-planner-scheduling`

### Run tests

`python3 -m unittest tests.test_model.TestCalculations`

### Start dev server

`python3 src.main.py`

### Start prod server

`gunicorn -w 2 src.main:app -b 0.0.0.0:8082`

### API

`http://localhost:8082/v1/scheduleTasks`


Example request body:

```json

{
    "tasks": [
        {
            "id": "B1",
            "name": "Naprawić buga w feature A",
            "projectId": "B",
            "priority": 4,
            "startTime": null,
            "duration": 3
        },
        {
            "id": "B2",
            "name": "Testy jednostkowe do feature A",
            "projectId": "B",
            "priority": 3,
            "startTime": null,
            "duration": 3
        },
        {
            "id": "B3",
            "name": "Przeanalizować wymagania do feature X",
            "projectId": "B",
            "priority": 1,
            "startTime": null,
            "duration": 2
        },
        {
            "id": "C1",
            "name": "Bieganie",
            "projectId": "C",
            "priority": 3,
            "startTime": null,
            "duration": 1
        },
        {
            "id": "C2",
            "name": "Czytanie",
            "projectId": "C",
            "priority": 2,
            "startTime": null,
            "duration": 0
        },
        {
            "id": "C3",
            "name": "Pianino",
            "projectId": "C",
            "priority": 1,
            "startTime": null,
            "duration": 1
        },
        {
            "id": "A1",
            "name": "Odkurzyć",
            "projectId": "A",
            "priority": 1,
            "startTime": null,
            "duration": 0
        },
        {
            "id": "A2",
            "name": "Duże zakupy",
            "projectId": "A",
            "priority": 2,
            "startTime": null,
            "duration": 1
        },
        {
            "id": "A3",
            "name": "Wizyta internista",
            "projectId": "A",
            "priority": 4,
            "startTime": 12.0,
            "duration": 1
        },
        {
            "id": "A4",
            "name": "Przygotować obiad na kolejne dni",
            "projectId": "A",
            "priority": 2,
            "startTime": null,
            "duration": 1
        },
        {
            "id": "D1",
            "name": "Medytacja",
            "projectId": "D",
            "priority": 3,
            "startTime": null,
            "duration": 0
        },
        {
            "id": "D2",
            "name": "Spacer",
            "projectId": "D",
            "priority": 2,
            "startTime": null,
            "duration": 0
        }
    ],
    "projects": [
        {
            "timeRangeStart": 8.0,
            "timeRangeEnd": 10.0,
            "id": "D",
            "name": "morning"
        },
        {
            "timeRangeStart": 0.0,
            "timeRangeEnd": 24.0,
            "id": "A",
            "name": "default"
        },
        {
            "timeRangeStart": 9.0,
            "timeRangeEnd": 17.0,
            "id": "B",
            "name": "work"
        },
        {
            "timeRangeStart": 17.0,
            "timeRangeEnd": 22.0,
            "id": "C",
            "name": "hobby"
        }
    ],
    "bannedRanges": [
        {
            "timeRangeStart": 0.0,
            "timeRangeEnd": 8.0,
            "id": "R1"
        },
        {
            "timeRangeStart": 22.0,
            "timeRangeEnd": 24.0,
            "id": "R2"
        }
    ]
}

```