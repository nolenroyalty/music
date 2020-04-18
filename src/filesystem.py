import os
import subprocess
from pathlib import Path
import src.util as util

@util.lazy
def repo_root():
    path = subprocess.Popen( ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE).communicate()[0].rstrip().decode()
    return Path(path)

def artist_directory(artist):
    base = repo_root()
    return base.joinpath("data", artist.filename())

def ensure_artist_directory_exists(artist):
    artist_directory(artist).mkdir(parents=True, exist_ok=True)

def path_to_data_file(artist, album):
    directory = artist_directory(artist)
    album_file = "{}.json".format(album.filename())
    return directory.joinpath(album_file)
