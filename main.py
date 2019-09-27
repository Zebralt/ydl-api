import asyncio
import os
import re
import time
from functools import partial, wraps
from random import randrange

from quart import Quart

import download as dl

from asciitable import p as atable


app = Quart(__name__)
app.post = partial(app.route, methods=['POST'])
app.get = partial(app.route, methods=['GET'])


@app.post('/list')
async def list_songs():
    return ''
  

@app.get('/tasks')
async def list_tasks():
    data = [
        dict(
            tid=key,
            **value
        )
        for key, value in dl.TASKS.items()
    ]

    if not data:
        return ''
    
    v = atable(
        data[0].keys(),
        [list(d.values()) for d in data],
        sizes=30
    ).replace('\n', '<br/>')

    v = v.strip()
    v = re.sub(r'\x1b\[[0-9;a-z]*?m', '', v)
    v = v.replace(' ', '&nbsp;')

    v = f"""
    <html style='font-family:monospace; color: white; background-color: black'>
    {v}
    </html>
    """


    return v


@app.get('/ls')
async def list_files():
    return '<br/>'.join(os.listdir('/music'))


async def save(tid):

    with open(f"/music/{tid}.log", "w+") as f:
        f.write("1")

    await asyncio.sleep(5)

    dl.TASKS[tid]['status'] = 'Success'

    return tid

  
@app.get('/download')
async def download_song():
    
    tid = time.time() + randrange(300)
    task = {}
    dl.TASKS[tid] = task

    task['target'] = tid
    task['status'] = 'In process'

    asyncio.ensure_future(save(tid))

    return str(tid)


@app.get('/')
async def home():
    return 'Hello world!'
    