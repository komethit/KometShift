import json

with open('./settings/settings.json', 'r') as file1: prefs = json.load(file1)
with open('./settings/themes/theme.json', 'r') as file2: theme = json.load(file2)
with open('./settings/run.json', 'r') as file3: run = json.load(file3)
with open('./settings/lang/lang.json', 'r') as file4: lang = json.load(file4)
with open('./settings/keys.json', 'r') as file5: keys = json.load(file5)