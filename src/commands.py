import argparse
import sys
from pathlib import Path
from src.music_attribute import Artist, Album
from src.music_entry import MusicEntry
from src.util import yes_or_no
from src.search_filter import Filter
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
    def print_entry(filename):
        if args.json:
            print(entry.to_json())
        else:
            print(entry.to_string_simple())

    filters = [Filter(f) for f in args.filter]

    entries = [
        MusicEntry.load(file_) for file_ in filesystem.list_files(artist=args.artist)
    ]
    db = MusicDB(entries, filters)
    for entry in db:
        print_entry(entry)


def set_search_args(sub):
    search_parser = sub.add_parser("search")
    search_parser.add_argument("--artist", "-a", help="Search for artist")
    search_parser.add_argument(
        "--json", "-j", action="store_true", help="Show json instead of summary"
    )
    search_parser.add_argument(
        "--filter",
        "-f",
        nargs="*",
        default=[],
        help="Search filter ($var([><=]|!=)$value)",
    )
    search_parser.set_defaults(func=search_albums)


def validate(args):
    filenames = filesystem.list_files(artist=args.artist)
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
