import urllib.request, json 
from settings import prefs

def checkversionyes() -> bool:
    with urllib.request.urlopen("https://api.npoint.io/a13b3514a72477ecd6f5") as url:
        data = json.load(url)
    if data['version'] == prefs['editor']['window']['version']:return 1
    else:return 0