from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import webhook, devices

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from prometheus_fastapi_instrumentator import Instrumentator

import logging
import sys

app = FastAPI()

# region logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
# endregion logging

# region add prometheus instrumentation
Instrumentator().instrument(app).expose(app)
# endregion


# region add endpoints
# webhook end-points
app.include_router(webhook.webhook_ep)

# nornir/naplam end-points
app.include_router(devices.devices_ep)

# configure /static
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# endregion


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('startup')

    try:
        # add anything that need to be performed on startup such as table creations
        pass
    except Exception as ex:
        print(ex)


@app.get('/')
async def default():
    """redirect to /docs"""
    response = RedirectResponse(url='/docs')
    return response


if __name__ == '__main__':
    """if called as a command line app"""
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description='fastAPI webhook')
    parser.add_argument('-p', '--port', help='listener port', default=8000, type=int)
    args = parser.parse_args()

    uvicorn.run("main:app", host="0.0.0.0", port=args.port, log_level="debug", reload=True)
