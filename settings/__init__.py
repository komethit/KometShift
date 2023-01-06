import json

with open("./settings/settings.json", "r") as prefFile:
    pre = prefFile.read()


class Settings(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


pref = Settings(pre)

with open("./settings/theme/theme.json", "r") as themFile:
    the = themFile.read()


class Theme(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


theme = Theme(the)

with open("./settings/lang/lang.json", "r") as lanFile:
    lang = json.load(lanFile)

with open("./settings/keys.json", "r") as keyFile:
    keys = json.load(keyFile)

with open("./settings/debug/run.json", "r") as runFile:
    run = json.load(runFile)
