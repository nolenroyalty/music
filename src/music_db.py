import src.filesystem as filesystem
from src.music_entry import MusicEntry
from collections import defaultdict


class MusicDB:
    def __init__(self, all_entries, filters):
        def matches(entry):
            return all(f.matches(entry) for f in filters)

        self.all = [entry for entry in all_entries if matches(entry)]
        self.by_artist = defaultdict(list)
        for entry in self.all:
            artist = entry.artist.value
            self.by_artist[artist].append(entry)

    @staticmethod
    def load():
        entries = [MusicEntry.load(filename) for filename in filesystem.list_files()]
        MusicDB(entries)

    def entries(self):
        return self.all_entries

    def __iter__(self):
        return iter(self.all)
