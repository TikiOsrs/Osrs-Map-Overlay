import requests
import shutil

map_orb_image_names = "https://maps.runescape.wiki/osrs/data/iconLists/MainIcons.json"
map_orb_image_icons = "https://maps.runescape.wiki/osrs/images/icons/"

def download_orb(orbName):
    orb = map_orb_image_icons + orbName
    r = requests.get(orb, stream=True)
    if r.status_code == 200:
        with open(f'./resources/mapOrbs/{orbName}', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw,f)
        print(f"Done with {orbName}")
    else:
        print(f"Trouble downloading {orbName} - status code {r.status_code}")


orbImageResponse = requests.get(map_orb_image_names)
orbFileNames = orbImageResponse.json().get("icons")
for fileName in orbFileNames:
    orbObject = orbFileNames.get(fileName)
    print(f'Downloading Orb - {orbObject.get("name")}')
    download_orb(orbObject.get("filename"))
