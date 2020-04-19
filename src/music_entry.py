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


def assert_is_attribute(arg):
    if issubclass(arg.__class__, MusicAttribute):
        return
    else:
        raise Exception("Expected {} to be a MusicAttribute".format(type(arg)))


class MusicEntry:
    def __init__(self, *args, **kwargs):
        args = list(args) + list(kwargs.values())
        for arg in args:
            assert_is_attribute(arg)
            setattr(self, arg._machine_name, arg)

    def to_json(self, indent=2):
        return json.dumps(self.__dict__, cls=MusicEncoder, indent=indent)

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def create(cls, **kwargs):
        for (name, value) in kwargs.items():
            attr = MusicAttribute.create_by_name(name, value)
            kwargs[attr._machine_name] = attr

        return MusicEntry(**kwargs)

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
        for attribute in MusicAttribute.__subclasses__():
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
        return filesystem.path_to_data_file(self.artist, self.album)

    def save(self):
        filesystem.ensure_artist_directory_exists(self.artist)
        path = self.path_in_repo()
        with open(path, "w") as f:
            f.write(self.to_json())

    def edit(self):
        for attribute in MusicAttribute.__subclasses__():
            if yes_or_no("Would you like to edit {}? ".format(attribute._human_name)):
                edited = getattr(self, attribute._machine_name).edit()
                setattr(self, attribute._machine_name, edited)
