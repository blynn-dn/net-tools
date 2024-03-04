"""
This is simple example of how to receive a webhook event from netbox
"""
import logging

from fastapi import APIRouter, Depends
from app.dependencies import get_x_hook_signature_header
from app.models import AnyJson
from app.models.netbox import EventRoot as NetboxRootEvent
from app.provisioning.dns import DNSTools

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create /webhook API router endpoint
webhook_ep = APIRouter(
    prefix='/webhook',
    dependencies=[Depends(get_x_hook_signature_header)],
    tags=['webhook'],
    responses={404: {'description': 'Not Found'}}
)


@webhook_ep.post('/device')
async def post_device_message(body: NetboxRootEvent):
    """simple netbox webhook event receiver"""

    # log the event
    logger.info(f"event: {body}")

    """
    Do something with the `event`.  Typical use case is to perform asynchronous processing.  For example:
        * publish to a queue, topic for additional processing
        * publish the event as a Celery task
        * persist the vent to a database 
        * send a notification message such as to Slack, SNS, Lambda function, etc.
    """
    return "ok"


@webhook_ep.post('/ip_address')
async def post_ip_address(body: NetboxRootEvent):
    """simple netbox webhook event receiver"""

    # log the event
    logger.info(f"event: {body}")

    print(f"event: {body.root.event_type}")
    print(f"model: {body.root.model}")
    print(body.root.snapshots.pre_change)
    print(body.root.snapshots.post_change)

    """
    Do something with the `event`.  Typical use case is to perform asynchronous processing.  For example:
        * publish to a queue, topic for additional processing
        * publish the event as a Celery task
        * persist the vent to a database 
        * send a notification message such as to Slack, SNS, Lambda function, etc.
    """
    DNSTools(body.root).process()
    return "ok"
