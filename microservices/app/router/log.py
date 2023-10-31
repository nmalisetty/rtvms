import json
from datetime import datetime

from fastapi import APIRouter, HTTPException,Request
from fastapi.param_functions import File, Form
from typing import Any
from .model_conditions import DetectiveModel
from .invoke_serives import *
from pydantic import BaseModel,ValidationError


router = APIRouter()
model = DetectiveModel()

class StreamingData(BaseModel):
    source: str
    id: Any
    timeStamp: datetime
    data: Any
    type: str
    crash:bool


@router.post("/edge/streaming_data")
async def receive_streaming_data( data: StreamingData):
    try:
        data = json.loads(data.json())

        result = model.investigate(data["crash"],data["data"])
        if(result):
            if(result["Beacon"]):
                send_beacon_kafka(None,data["id"],"http://localhost:8000/producer/beacons")
            else:
                send_alert_kafka(result["Message"],data["id"],"http://localhost:8000/producer/alerts")
            return {"Status": "Alerts raised"}
        else:
            return {"Status":"All OK"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.json())

@router.post("/log")
async def log_file(file: bytes = File(...), filename: str = Form(...)):
    try:
        # Parse the JSON file
        json_file = json.loads(file)

        print(json_file)
        # Log the file
        with open(filename, 'w') as f:
            json.dump(json_file, f)

        return {"message": "File logged successfully."}
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
