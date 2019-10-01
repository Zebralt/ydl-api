import asyncio
import os
import re
import time
from functools import partial
from random import randrange

from quart import Quart
from quart_cors import cors

import download as dl

from asciitable import p as atable


app = Quart(__name__)
app = cors(app, allow_origin='*')
app.post = partial(app.route, methods=['POST'])
app.get = partial(app.route, methods=['GET'])


colors = {
    0: 'black',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'blue',
    5: 'violet',
    6: 'lightblue',
    7: 'white'
}


@app.post('/list')
async def list_songs():
    return ''


def get_css_color(codes):
    codes = codes.strip()
    codes = codes.split(';')

    for idx, code in enumerate(codes):

        c = int(code)
        t = 'color: {};'
        if c in range(40, 48) or c in range(100, 108):
            t = 'background-' + t
        t = t.format(colors.get(c, 'black'))

        codes[idx] = t

    print(codes)

    return ';'.join(codes)


def color_escape_to_html(text):

    regex = r'\x1b\[([\w;]*?)m(.*?\x1b\[0?m)'

    # otext = text

    print(repr(text))

    m = re.match(regex, text)

    while m:
        a, b = m.span()
        color, inner = m.groups()
        before, after = text[:a], text[b:]

        css_color = get_css_color(color)

        text = f'{before} <span color="{css_color}"> {inner} </span> {after}'
    return text


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
        return """<html style='font-family:monospace; color: white; background-color: black'>
            </html>"""

    v = atable(
        data[0].keys(),
        [list(d.values()) for d in data],
        sizes=30
    ).replace('\n', '<br/>')

    v = v.strip()
    # v = re.sub(r'\x1b\[[0-9;a-z]*?m', '', v)
    v = color_escape_to_html(v)
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
    dl.TASKS[tid]['file'] = 'file.mp3'

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


from htmlize import m


@app.get('/')
async def home():
    return m.html(
        m.body(
            m.input(type="text"),
            m.button("This is Sparta!")
        ),
        style="background-color: black; color: white"
    )
