import os
import glob
import math

import jinja2
from mutagen.oggvorbis import OggVorbis


TEMPLATE_PATH = "template.html"
SONG_PATTERN = "assets/audio/*.ogg"


def format_length(seconds):
    mins = int(seconds / 60)
    remainder = int(seconds - mins * 60)
    return "{}:{:02d}".format(mins, remainder)


def fetch_song_metadata(pattern):
    songs = []
    for href in glob.glob(pattern):
        title = os.path.splitext(os.path.basename(href))[0]
        length = format_length(OggVorbis(href).info.length)
        songs.append(dict(href=href, title=title, length=length))
    return songs


def render_template(path, kwargs):
    with open(path, "r") as f:
        template = jinja2.Template(f.read())
    return template.render(**kwargs)


def write_index(html, path="index.html"):
    with open(path, "w") as f:
        f.write(html)


if __name__ == "__main__":
    songs = fetch_song_metadata(SONG_PATTERN)
    render_kwargs = dict(songs=songs)
    html = render_template(TEMPLATE_PATH, render_kwargs)
    write_index(html)
