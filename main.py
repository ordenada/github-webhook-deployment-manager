from dotenv import load_dotenv

load_dotenv()

import os
import hmac
import hashlib

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import Response
import uvicorn

from classes.controllers.push_controller import push_controller
from classes.log import logger

app = FastAPI()

SECRET = os.environ['SECRET']


def taskable_push_controller(data: dict):
    try:
        push_controller(data)
    except Exception as err:
        logger.error('Cannot run the "push" controller')
        logger.error(err)


def verify_signature(payload_body: bytes, secret_token: str, signature_header: str):
    if not signature_header:
        raise HTTPException(
            status_code=403,
            detail='x-hub-signature-256 header is missing!',
        )
    
    hash_object = hmac.new(
        secret_token.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256,
    )

    expected_signature = f'sha256={hash_object.hexdigest()}'
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(
            status_code=403,
            detail='Request signatures didn\'t match!',
        )


@app.post('/webhook')
async def process_webhook(request: Request, background_tasks: BackgroundTasks):
    signature_header = request.headers.get('X-Hub-Signature-256')
    event_type = request.headers.get('X-GitHub-Event')
    raw = await request.body()

    verify_signature(raw, SECRET, signature_header)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        raise HTTPException(status_code=415, detail='Content-Type must be application/json')

    data = await request.json()
    logger.debug('event_type:', event_type)
    logger.debug(data)

    # handler event
    if event_type == 'push':
        background_tasks.add_task(taskable_push_controller, data)


    return Response(status_code=204)


if __name__ == '__main__':
    HOST = os.environ.get('HOST', 'localhost')
    PORT_STR = os.environ.get('PORT', '3000')
    PORT = int(PORT_STR)
    logger.debug('Starting in %s:%d', HOST, PORT)
    uvicorn.run(app, host=HOST, port=PORT)
