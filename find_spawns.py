import json
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def spawn_single_lookup(item: str):
    """
    spawn_single_lookup takes an item name and queries the osrs wiki for all spawns. 
    """
    # Make an empty object to hold all spawns of same type
    spawn_locations = { 
        "item" : item,
        "spawns" : []
    }

    #Query wiki for object name
    response = requests.get(f'https://oldschool.runescape.wiki/api.php?action=query&format=json&formatversion=2&titles={item}&prop=mapdata&mpdlimit=max&mpdgroups=pins')
    #Parse out the json response for all spawns.
    spawns = json.loads(response.json()["query"]["pages"][0]["mapdata"][0])["pins"]
    #if there are spaws
    if spawns:
        #For each Spawn
        for spawn in spawns:
            #create a temp object 
            #add location data for each object,
            for feature in spawn.get("features"):
                temp = {}
                #grab X, and Y location
                temp["x"] = feature["geometry"]["coordinates"][0]
                temp["y"] = feature["geometry"]["coordinates"][1]
                #Split up all description tags
                descriptions = feature["properties"]["description"].split("<b>")
                for description in descriptions:
                    #Find the quantity tag from decriptions and append it to object
                    if "quantity" in description.lower():
                        temp["quantity"] = re.sub('[^0-9]','', description)
                spawn_locations["spawns"].append(temp)
                if temp["x"] >= 3231 and temp["y"] >= 3218:
                    if temp["x"] <= 3237 and temp["y"] <= 3229:
                        print("Weird Spawn:",item,feature)
    return [spawn_locations]

def spawn_all_locations(f2p):
    spawns = []
    #Pull all objects from Item_Spawns
    response = requests.get("https://oldschool.runescape.wiki/w/Item_spawn")
    #Parse out the HTML
    soup = BeautifulSoup(response.content.decode("UTF-8"),"html.parser")
    #Find the class that contains all the objects
    main = soup.find("div","mw-parser-output") 
    # Grab all list objects
    items = [item.a.text.replace(" ","_") for item in main.find_all("li")]
    # Run through all items found individually.
    for item in items:
        if f2p:
            if spawn_item_f2p(item):
                spawns.extend(spawn_single_lookup(item))
        else:
            spawns.extend(spawn_single_lookup(item))
    return spawns

def spawn_item_f2p(item): 
    response = requests.get(f"https://oldschool.runescape.wiki/w/{item}")
    soup = BeautifulSoup(response.content.decode("UTF-8"),"html.parser")
    main = soup.find("table", "infobox no-parenthesis-style infobox-item")
    if not main:
        main = soup.find("table", "infobox infobox-switch infobox-item")
    if not main:
        main = soup.find("table", "infobox infobox-item")
    if not main:
        main = soup.find("table", "infobox infobox-switch no-parenthesis-style infobox-item")
    for row in main.tbody.find_all('tr'):
        attribute = row.find('th')
        value = row.find('td')
        if attribute and value:
            if attribute.text == "Members":
                if value.text.strip() == "No":
                    return True
                if value.text.strip() == "Yes":
                    return False
        
