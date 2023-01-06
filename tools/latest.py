import json


def loadLatest():
    with open("./cache/latest.json") as file7:
        a = json.loads(file7.read())
        return a


def writeLatest(obj):
    with open("./cache/latest.json", "w") as file:
        json.dump(obj, file, indent=4)
