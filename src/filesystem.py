import os
import subprocess
from pathlib import Path
from functools import lru_cache
import src.util as util


@lru_cache(maxsize=1)
def repo_root():
    path = (
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .rstrip()
        .decode()
    )
    return Path(path)


def data_dir():
    return repo_root().joinpath("data")


# nroyalty: it's confusing that this takes an Artist but
# the below function takes a string
def artist_directory(artist):
    return data_dir().joinpath(artist.filename())


def ensure_artist_directory_exists(artist):
    artist_directory(artist).mkdir(parents=True, exist_ok=True)


def path_to_data_file(artist, album):
    directory = artist_directory(artist)
    album_file = "{}.json".format(album.filename())
    return directory.joinpath(album_file)


def is_data_file(file_):
    return file_.is_file() and (file_.suffix == ".json")


def directories(path):
    return (d for d in path.iterdir() if d.is_dir())


def data_files(path):
    return (f for f in path.iterdir() if is_data_file(f))


def _list():
    base = data_dir()
    for directory in directories(base):
        for file_ in data_files(directory):
            yield file_


def _list_artist(artist):
    directory = data_dir().joinpath(artist)
    for file_ in data_files(directory):
        yield file_


@lru_cache(maxsize=None)
def list_files(artist=None):
    if artist is not None:
        return _list_artist(artist)
    else:
        return _list()
