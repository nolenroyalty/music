import json
import re
from src.util import yes_or_no, filenameable


class MusicAttribute:
    # nroyalty: It'd be fun to derive machine name by parsing
    # the class name and adding underscores where there are
    # uppercase characters but like, why.
    _machine_name = None
    _human_name = None
    _prompt = None
    _of_string = None
    _validate = None

    def __init__(self, value):
        validate = self._validate
        if validate is not None:
            validate(value)

        self.value = value

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def create_interactive(cls):
        while True:
            response = input("{} ".format(cls._prompt))
            try:
                value = cls._of_string(response)
                break
            except ValueError as e:
                print("That didn't parse - {}. Try again".format(e))

        return cls(value)

    def set(self, value):
        self.value = value
        return self

    def edit(self):
        prompt = "Current {}: {}\nEnter a new {}: ".format(
            self._human_name, self.value, self._human_name
        )
        while True:
            try:
                value = self._of_string(input(prompt))
                self.value = value
                return self
            except ValueError as e:
                if yes_or_no("That didn't parse - {}.  Try again?".format(e)):
                    pass
                else:
                    return self

    def display(self):
        return "{}: {}".format(self.human_name, self.value)

    def filename(self):
        return filenameable(self.value)

    @classmethod
    def create_by_name(cls, name, value):
        name = name.lower()
        for subclass in cls.__subclasses__():
            if name == subclass._machine_name or name == subclass._human_name.lower():
                return subclass(value)
        raise Exception("Could not find an attribute with name {}".format(name))

    @classmethod
    def create_of_string(cls, name, value):
        name = name.lower()
        for subclass in cls.__subclasses__():
            if name == subclass._machine_name or name == subclass._human_name.lower():
                return subclass(subclass._of_string(value))
        raise Exception("Could not find an attribute with name {}".format(name))

    @staticmethod
    def normalize(x):
        if isinstance(x, str):
            return x.lower()
        return x

    def __eq__(self, other):
        return self.normalize(self.value) == self.normalize(other.value)

    def __ne__(self, other):
        return self.normalize(self.value) != self.normalize(other.value)

    def __lt__(self, other):
        return self.normalize(self.value) < self.normalize(other.value)

    def __gt__(self, other):
        return self.normalize(self.value) > self.normalize(other.value)

    def __le__(self, other):
        return self.normalize(self.value) <= self.normalize(other.value)

    def __ge__(self, other):
        return self.normalize(self.value) >= self.normalize(other.value)


class Artist(MusicAttribute):
    _machine_name = "artist"
    _human_name = "Artist"
    _prompt = "Who is the artist?"

    @classmethod
    def _of_string(cls, s):
        return str(s)


class Album(MusicAttribute):
    _machine_name = "album"
    _human_name = "Album"
    _prompt = "What is the album name?"

    @classmethod
    def _of_string(cls, s):
        return str(s)


class Genres(MusicAttribute):
    _machine_name = "genres"
    _human_name = "Genres"
    _prompt = "What genre(s) would you say this is?"

    @classmethod
    def _of_string(cls, s):
        genres = re.split(r"[,/]", s)
        return [s.strip().lower() for s in genres]

    def __eq__(self, other):
        ours = [self.normalize(v) for v in self.value]
        other = [self.normalize(v) for v in other.value]
        return any(genre in ours for genre in other)


class YearMade(MusicAttribute):
    _machine_name = "year_made"
    _human_name = "Year Made"
    _prompt = "What year was the album made?"

    @classmethod
    def _of_string(cls, s):
        return int(s)


class YearFound(MusicAttribute):
    _machine_name = "year_found"
    _human_name = "Year Found"
    _prompt = "In what year did you find this album?"

    @classmethod
    def _of_string(cls, s):
        return int(s)


class YearsImportant(MusicAttribute):
    _machine_name = "years_important"
    _human_name = "Years Important"
    _prompt = "In what years has this album been important to you?"

    @classmethod
    def _of_string(cls, s):
        years = []
        for year in s.split(","):
            maybe_separated = year.split("-")
            if len(maybe_separated) == 1:
                years.append(int(year))
            elif len(maybe_separated) == 2:
                start = int(maybe_separated[0])
                end = int(maybe_separated[1])
                for year in range(start, end + 1):
                    years.append(year)
            else:
                raise ValueError("Why'd you use two dashes, bud?")

        return years


class HowFound(MusicAttribute):
    _machine_name = "how_found"
    _human_name = "How the album was found"
    _prompt = "How did you find this album?"

    @classmethod
    def _of_string(cls, s):
        # CR nroyalty: This should do some smart stuff to normalize
        # things like spotify, pitchfork, etc
        return s


class FreeForm(MusicAttribute):
    _machine_name = "free_form"
    _human_name = "Free Form"
    _prompt = "Enter anything else you'd like to say about this album (or just hit enter if you don't want to write anything)"

    @classmethod
    def _of_string(cls, s):
        if s == "":
            return None
        return s
