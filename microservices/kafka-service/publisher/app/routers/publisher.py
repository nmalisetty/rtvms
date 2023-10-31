import json

from app.core.gateways.kafka import Kafka
from app.core.models.message import AlertRequest, BeaconRequest, AckRequest

from fastapi import APIRouter, Depends
from app.dependencies.kafka import get_kafka_instance

router = APIRouter()


@router.post("/alerts")
async def send_alerts(data: AlertRequest, server: Kafka = Depends(get_kafka_instance)):
    try:
        await server.aioproducer.send_and_wait('alerts', json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await server.aioproducer.stop()
        raise e
    return 'Alert sent successfully'


@router.post("/beacons")
async def send_beacons(data: BeaconRequest, server: Kafka = Depends(get_kafka_instance)):
    try:
        await server.aioproducer.send_and_wait('beacons', json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await server.aioproducer.stop()
        raise e
    return 'Beacon sent successfully'


@router.post("/acks")
async def send_acks(data: AckRequest, server: Kafka = Depends(get_kafka_instance)):
    try:
        await server.aioproducer.send_and_wait('beacons', json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await server.aioproducer.stop()
        raise e
    return 'Acknowledgement sent successfully'
