from functools import partial, wraps
import asyncio
from quart import Quart
import time
from random import randrange

import download as dl


app = Quart(__name__)
app.post = partial(app.route, methods=['POST'])
app.get = partial(app.route, methods=['GET'])


@app.post('/list')
async def list_songs():
    return ''
  

@app.get('/tasks')
async def list_tasks():
    return '<br/>'.join(map(str, dl.TASKS.items()))

  
@app.get('/download')
async def download_song():
    
    tid = time.time() + randrange(300)
    task = {}
    dl.TASKS[tid] = task

    task['target'] = tid
    task['status'] = 'In process'

    await asyncio.sleep(2)

    task['status'] = 'Success'

    return ''


@app.get('/')
async def home():
    return 'Hello world!'
    