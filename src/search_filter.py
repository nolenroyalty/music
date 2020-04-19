from src.music_attribute import MusicAttribute
import re


class Operation:
    ops = {"=", "==", "!=", ">", ">=", "<", "<="}
    op_rex = "({})".format("|".join(ops))

    def __init__(self, s):
        if s in self.ops:
            self.op = s
        else:
            raise Exception("Did not recognize operation {}".format(s))

    def matches(self, criteria, value):
        if self.op == "=":
            return value == criteria
        if self.op == "==":
            return value == criteria
        if self.op == "!=":
            return value != criteria
        if self.op == ">":
            return value > criteria
        if self.op == "<":
            return value < criteria
        if self.op == ">=":
            return value >= criteria
        if self.op == "<=":
            return value <= criteria
        raise Exception("How did you get here")


class Filter:
    rex = r"^([a-zA-Z_]+){}([\w\s]+)$".format(Operation.op_rex)

    def __init__(self, s):
        match = re.match(self.rex, s)
        if match is None:
            raise Exception("Couldn't parse filter {}.  rex: {}".format(s, self.rex))

        attr = match.group(1)
        value = match.group(3)
        self.attr = MusicAttribute.create_by_name(attr, value)
        self.op = Operation(match.group(2))

    def matches(self, candidate):
        # I mean, if it works
        name = self.attr._machine_name
        candidate = getattr(candidate, name)
        return self.op.matches(self.attr, candidate)
