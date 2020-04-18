import argparse
import sys
from pathlib import Path
from src.music_attribute import Artist, Album
from src.music_entry import MusicEntry
from src.util import yes_or_no
import src.filesystem

def add_args():
    parser = argparse.ArgumentParser(prog="ADD ENTRY")
    return parser

def add(args):
    artist = args.artist
    album = args.album

    filename = filesystem.path_to_data_file(artist, album)

    # CR-soon nroyalty: typo-spot here on artist 
    if filename.exists():
        entry = MusicEntry.load(filename)
        print("An entry for that album already exists:")
        print(entry.to_json())
        if not yes_or_no("Edit that entry instead?"):
            print("Ok, exiting.")
            sys.exit(0)

        entry.edit()
    else:
        pre_filled_attributes = [args.artist, args.album]
        entry = MusicEntry.create_interactive(pre_filled_attributes=pre_filled_attributes)

    print("Cool, here's your guy:")
    print(entry.to_json())
    if yes_or_no("Save that sucker?"):
        filesystem.ensure_artist_directory_exists(artist)
        with open(filename, 'w') as f:
            f.write(entry.to_json())
    else:
        print("Cool, exiting.")
        sys.exit(0)

def get_parser():
    parser = argparse.ArgumentParser(prog="MUSIC.EXE")
    sub = parser.add_subparsers()
    # Add new music
    add_parser = sub.add_parser("add")
    add_parser.add_argument("artist", help="Artist to add", type=Artist)
    add_parser.add_argument("album", help="Album to add", type=Album)
    add_parser.set_defaults(func=add)
    return parser

