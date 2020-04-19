import re


def yes_or_no(prompt):
    prompt = "{} [y/n] ".format(prompt)
    while True:
        response = input(prompt).lower()
        if response == "y":
            return True
        elif response == "n":
            return False 

def filenameable(s):
    return re.sub(r"[^A-Za-z0-9_-]+", "", s.replace(" ", "-")).lower()
