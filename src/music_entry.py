import json
from src.music_attribute import (
    MusicAttribute,
    Artist,
    Album,
    Genres,
    YearMade,
    YearFound,
    YearsImportant,
    HowFound,
    FreeForm,
)
from src.util import yes_or_no
import src.filesystem as filesystem


class MusicEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MusicAttribute):
            return obj.value
        return json.JSONEncoder.default(self, obj)


class MusicEntry:
    _attributes = [
        Artist,
        Album,
        Genres,
        YearMade,
        YearFound,
        YearsImportant,
        HowFound,
        FreeForm,
    ]

    def __init__(
        self,
        artist,
        album,
        genres,
        year_made,
        year_found,
        years_important,
        how_found,
        free_form,
    ):
        self.artist = artist
        self.album = album
        self.genres = genres
        self.year_made = year_made
        self.year_found = year_found
        self.years_important = years_important
        self.how_found = how_found
        self.free_form = free_form

    def to_json(self, indent=2):
        return json.dumps(self.__dict__, cls=MusicEncoder, indent=indent)

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def create(
        cls,
        artist,
        album,
        genres,
        year_made,
        year_found,
        years_important,
        how_found,
        free_form=None,
    ):
        return MusicEntry(
            artist=Artist(artist),
            album=Album(album),
            genres=Genres(genres),
            year_made=YearMade(year_made),
            year_found=YearFound(year_found),
            years_important=YearsImportant(years_important),
            how_found=HowFound(how_found),
            free_form=FreeForm(free_form),
        )

    @classmethod
    def create_interactive(cls, pre_filled_attributes=None):
        if pre_filled_attributes is None:
            pre_filled_attributes = []

        def maybe_use_pre_filled_attribute(candidate):
            for attribute in pre_filled_attributes:
                if isinstance(attribute, candidate):
                    return attribute
            return None

        values = {}
        for attribute in MusicEntry._attributes:
            pre_filled = maybe_use_pre_filled_attribute(attribute)
            if pre_filled is None:
                attribute = attribute.create_interactive()
            else:
                attribute = pre_filled
            values[attribute._machine_name] = attribute

        return MusicEntry(**values)

    def validate(self):
        # CR-soon nroyalty
        pass

    def to_string_simple(self):
        return "{} - {} ({})".format(
            self.artist.value, self.album.value, self.year_made.value
        )

    @staticmethod
    def _of_json(json):
        return MusicEntry.create(**json)

    @staticmethod
    def load(file_):
        with open(file_) as f:
            data = json.load(f)
            entry = MusicEntry._of_json(data)
            entry.validate()
            return entry

    @staticmethod
    def load_album_and_artist(album, artist):
        path = filesystem.path_to_data_file(artist, album)
        return self.load(path)

    def path_in_repo(self):
        filesystem.path_to_data_file(self.artist, self.album)

    def save(self):
        filesystem.ensure_artist_directory_exists(self.artist)
        path = self.path_in_repo()
        with open(path, "w") as f:
            f.write(self.to_json())

    def edit(self):
        for attribute in MusicEntry._attributes:
            if yes_or_no("Would you like to edit {}? ".format(attribute._human_name)):
                edited = getattr(self, attribute._machine_name).edit()
                setattr(self, attribute._machine_name, edited)
