import subprocess
import asyncio
import re
import os
from random import randrange
import time


URL_REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
MUSIC_LIBRARY = os.environ.get('MUSIC_LIBRARY') or '/music'
CMD = (
    "youtube-dl"
    " -x"  # Extract only audio
    " --audio-format mp3"  # In mp3 format
    " {url}"
    f" -o '{MUSIC_LIBRARY}/%(title)s.$(ext)s'" # Name the song after the video's title
)


TASKS = {
    0: {
        'target': 0,
        'status': 'Pending'
    }
}


async def download(url):

    if not re.match(URL_REGEX, url):
        raise ValueError("Not a valid URL")

    tid = time.time() + randrange(300)
    task = {}
    TASKS[tid] = task

    task['target'] = url
    task['status'] = 'In process'

    cmd = CMD.format(url=url).split()
    c = subprocess.check_output(cmd)
    print(c.decode('utf-8'))

    task['status'] = 'Success'


async def main():    
    url = 'https://www.youtube.com/watch?v=d19CLhpmmXg'
    await download(url)


if __name__ == "__main__":
    asyncio.run(main())