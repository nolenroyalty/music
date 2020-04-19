import src.filesystem as filesystem
from src.music_entry import MusicEntry
from collections import defaultdict

class MusicDB:
    def __init__(self, all_entries):
        self.all = all_entries
        self.by_artist = defaultdict(list)
        for entry in self.all:
            artist = entry.artist.value
            self.by_artist[artist].append(entry)

    @staticmethod
    def load():
        entries = [MusicEntry.load(filename) for filename in filesystem.list_files()]
        MusicDB(entries)

    def filter_artist(self, artist):
        MusicEntry(self.by_artist[artist])

    def filter_year_made(self, exact=None, min_year=None, max_year=None):
        filtered_entries = []
        for entry in self.all:
            year_made = entry.year_made.value
            exact_ok = exact is None or year_made == exact
            min_year_ok = min_year is None or year_made >= min_year
            max_year_ok = max_year is None or year_made <= max_year
            if exact_ok and min_year_ok and max_year_ok:
                filtered_entries.append(entry)

        return MusicDB(filtered_entries)

    def entries(self):
        return self.all_entries

    def __iter__(self):
        return iter(self.all)
