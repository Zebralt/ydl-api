from functools import partial, wraps

from flask import Flask, request


app = Flask(__name__)
app.post = partial(app.route, methods=['POST'])
app.get = partial(app.route, methods=['GET'])


@app.route('/list')
def list_songs():
    return ''
  
  
@app.route('/download')
@ratelimit(10, every=1)
def download_song():
    ...
    
    