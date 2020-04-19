import argparse
import sys
from pathlib import Path
from src.music_attribute import Artist, Album
from src.music_entry import MusicEntry
from src.util import yes_or_no
import src.filesystem as filesystem
from src.music_db import MusicDB



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
        entry = MusicEntry.create_interactive(
            pre_filled_attributes=pre_filled_attributes
        )

    print("Cool, here's your guy:")
    print(entry.to_json())
    if yes_or_no("Save that sucker?"):
        entry.save()
    else:
        print("Cool, exiting.")
        sys.exit(0)


def set_add_args(sub):
    add_parser = sub.add_parser("add")
    add_parser.add_argument("artist", help="Artist to add", type=Artist)
    add_parser.add_argument("album", help="Album to add", type=Album)
    add_parser.set_defaults(func=add)


def search_albums(args):
    full = args.full

    def print_entry(filename):
        if full:
            print(entry.to_json())
        else:
            print(entry.to_string_simple())

    entries = [MusicEntry.load(file_) for file_ in filesystem.list_files(artist=args.artist)]
    db = MusicDB(entries).filter_year_made(exact=args.year, min_year=args.min_year, max_year=args.max_year)

    for entry in db:
        print_entry(entry)


def set_search_args(sub):
    search_parser = sub.add_parser("search")
    search_parser.add_argument("--artist", "-a", help="Search for artist")
    search_parser.add_argument("--full", "-f", action="store_true", help="Show full json")
    search_parser.add_argument("--year", "-y",  type=int,  help="Show albums made in this year")
    search_parser.add_argument("--min-year", type=int, help="Earliest year album was made (inclusive)")
    search_parser.add_argument("--max-year", type=int, help="Latest year album was made (inclusive)")

    search_parser.set_defaults(func=search_albums)


def validate(args):
    filenames = filesystem.search_files(artist=args.artist)
    for filename in filenames:
        try:
            MusicEntry.load(filename)
        except Exception as e:
            print("{} doesn't parse - {}".format(filename, e))


def set_validate_args(sub):
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--artist", "-a", help="Just validate for artist")
    validate_parser.set_defaults(func=validate)


def get_parser():
    parser = argparse.ArgumentParser(prog="MUSIC.EXE")
    sub = parser.add_subparsers()
    set_add_args(sub)
    set_search_args(sub)
    set_validate_args(sub)
    return parser
