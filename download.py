import subprocess


MUSIC_LIBRARY = os.environ.get('MUSIC_LIBRARY') or 'd'



CMD = (
    "youtube-dl"
    " -x"  # Extract only audio
    " --audio-format mp3"  # In mp3 format
    " %s"
    " -o '%(title)s.$(ext)s'" # Name the song aft   er the video's title
)


def download(url):
    print(url)
    ydl.FileDownloader(

    )
if __name__ == "__main__":
    
    url = 'https://www.youtube.com/watch?v=d19CLhpmmXg'
    download(url)