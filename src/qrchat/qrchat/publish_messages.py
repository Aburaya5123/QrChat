from google.cloud import pubsub_v1
import os
from logging import getLogger
import json
from uuid import UUID
from .settings import MEDIA_ROOT


logger = getLogger(__name__)


def create_qrcode(url:str, room_uuid:UUID) -> str|None:
    try:
        project_id = os.environ.get("PROJECT_ID")
        topic_id = "main-topic"

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)

        message = json.dumps({'url':url, 'room_id':str(room_uuid)})
        data = message.encode("utf-8")
        future = publisher.publish(topic_path, data)

        return os.path.join(MEDIA_ROOT, f"{room_uuid}.png")
    except Exception as e:
        logger.error(e)
        return None
    

def delete_qrcode(room_uuid:UUID) -> None:
    try:
        project_id = os.environ.get("PROJECT_ID")
        topic_id = "main-topic"

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)

        message = json.dumps({'url':"del", 'room_id':str(room_uuid)})
        data = message.encode("utf-8")
        future = publisher.publish(topic_path, data)
    except Exception as e:
        logger.error(e)