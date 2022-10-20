from contextlib import nullcontext
import requests
import json
import requests
import re

def pull_object_data():
    """
    pull_object_data is a function that will download all the osrs object data, as well as all
    the object_morph data and reutrns both objects as a tuple.
    """
    objectsURL = "https://chisel.weirdgloop.org/moid/data_files/objectsmin.js"
    morphURL = "https://mejrs.github.io/data_osrs/object_morph_collection.json"

    objectList = []

    # Download the object_data
    objectsResponse = requests.get(objectsURL)
    # this downloads as a javascript array of objects, the below regext
    # grabs all objects within the array
    matches = re.findall(r'{[^\}]+}',objectsResponse.content.decode("UTF-8"))
    for match in matches:
        #parse out the object strings into json.
        objectList.append(json.loads(match))

    # Donwload Morph Data
    morphsResponse = requests.get(morphURL)
    morphs = morphsResponse.json()

    return (objectList,morphs)

def object_morph_lookup(id: str, morph_data):
    """
    object_morph_lookup iterates through all morphs for a specific ID and returns them.
    """
    results = [id]
    for item in morph_data.get(id,{}):
        results.append(str(item))
    return results

def object_location_lookup(id: str):
    """
    object_location_lookup takes an object id number as a string and returns information about it.
    
    """
    url = f'https://mejrs.github.io/data_osrs/locations/{id}.json'
    response = requests.get(url)
    # If ID isnt found retunr an empty object
    if (response.status_code != 200):
            return {}
    else:  
        output = response.json()
        return(output)

def object_search_by_id(id: str, object_data, morph_data):
    """
    object_search_by_id takes an id, and the object_data and morph_data to 
    combine the 3 different data sources of data on a single object and 
    adds all morphs and locations to the object. 
    """
    locations = []
    #iterate through all object data
    for object in object_data:
        
        # If the id of the object matches the argument id
        if str(object.get("id")) == id:
            #Add a morphs key to the current object with the output object_morph_lookup
            object["morphs"] = object_morph_lookup(id, morph_data)
            #For every morph found
            for morph in object["morphs"]:
                #Add all found objects of the found morphs to the object location.
                locations.extend(object_location_lookup(morph))
            object["locations"] = locations
            return [object]
    return [{}]

def object_search_by_substring(substring: str, object_data, morph_data): 
    """
    object_search_by_substring takes a substring as a string, this implements
    object_search_by_regex by adding the argument to an existing pattern. 
    """
    pattern = '[^\']{0,}'+substring+'[^\',]{0,}'
    return object_search_by_regex(pattern, object_data, morph_data)

def object_search_by_regex(pattern: str, object_data, morph_data): 
    """
    object_search_by_substring takes a pattern as a string, then iterates over
    all object names looking for any matches. 
    """
    output = []
    for object in object_data:
        if re.match(pattern,object.get("name"),re.IGNORECASE):
            output.extend(object_search_by_id(str(object.get("id")), object_data, morph_data))

    return output

