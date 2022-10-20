from xmlrpc.client import Boolean
from PIL import Image, ImageDraw, ImageFont
import requests, json, re
import os

font = ImageFont.load("./fontGen/ibmfont.pil")
map_border = 0
scale = 3
map_stary_y = 19
map_start_y = 39
image_origin_x = 18
image_origin_y = 196
chunk_size = 64
map_orb_locations = "https://maps.runescape.wiki/osrs/data/overlayMaps/MainMapIconLoc.json"
map_orb_image_names = "https://maps.runescape.wiki/osrs/data/iconLists/MainIcons.json"


def calc_origin_x(xCoord: int,xChunk = 0):
    finalX: int
    chunkOffset = (chunk_size*image_origin_x)
    #Turn Chunk to tiles
    finalX = (xChunk * chunk_size)
    # Add X Coord
    finalX += xCoord
    # Modify due to origin Change
    finalX = finalX - chunkOffset
    return finalX

def calc_origin_y(yCoord: int, yChunk = 0, ySize = 1):
    finalY: int
    chunkOffset = ((chunk_size*image_origin_y) + 63)
    # Turn Chunks to tiles
    finalY = (yChunk * chunk_size)
    # Add Y coord
    finalY += yCoord
    # Modify due to origin change
    finalY = (finalY - chunkOffset)
    # Invert due to origin change
    finalY = -1 * finalY
    #account for size
    finalY = finalY - (ySize - 1)
    return finalY

def calc_pixels(coord):
    return ((coord*scale)+map_border)


def object_draw_location(objectInfo, draw: ImageDraw, color: tuple):
    """
    object_draw_location takes an object that contains the object info, an ImageDraw Object, and a tuple of the RGB colors to color the objects.
    """
    #For every location found
    for location in objectInfo.get("locations",[]):
        #Grab the Size of the object found
        xSize = objectInfo["sizeX"]
        ySize = objectInfo["sizeY"]
        #if the object isnt a square, deal with rotation.
        if xSize != ySize:
            if location['rotation'] == 1:
                temp = ySize
                ySize = xSize
                xSize = temp
            elif location['rotation'] == 3:
                temp = ySize
                ySize = xSize
                xSize = temp
        #calculates x1,y1 and x2,y2
        x1 = calc_origin_x(location['x'],location['i'])
        y1 = calc_origin_y(location['y'],location['j'],ySize)
        x2 = x1 + xSize
        y2 = y1 + ySize
        # Draw the pixel
        draw.rectangle(((calc_pixels(x1), calc_pixels(y1)), 
                        (calc_pixels(x2)-1, calc_pixels(y2)-1)), 
                        fill=color)

def spawn_draw_location(spawns, draw: ImageDraw, color: tuple, labels = False):
    """
    Spawn_draw_location takes a spawns object, an ImageDraw object, a tuple for the colors, and if you want labels appended.
    """
    # For each spawn found
    for spawn in spawns["spawns"]:
        #Grab X and Y and plot them 
        x_spawn = spawn["x"]
        y_spawn = spawn["y"]
        x1 = calc_origin_x(x_spawn)
        y1 = calc_origin_y(y_spawn)
        draw.rectangle(
            ((calc_pixels(x1),calc_pixels(y1)), (calc_pixels(x1)+2,calc_pixels(y1)+2)), fill=color)
        # If the label flag is set, print out labels.
        if labels:
            draw.text((calc_pixels(x1+1) ,calc_pixels(y1-2)), f'{spawns["item"]} ({spawn.get("quantity")})', font=font, fill=color)

def map_add_all_location_orbs(map: Image):
    orbLocationsResponse = requests.get(map_orb_locations)
    orbImageResponse = requests.get(map_orb_image_names)
    orbFilenames = orbImageResponse.json().get("icons")

    for orb in orbLocationsResponse.json()["features"]:
        if orb.get("geometry",{}).get("coordinates")[2] == 0:
            orbFilename = orbFilenames.get(orb.get("properties",{}).get("icon")).get("filename")
            x = calc_origin_x(orb.get("geometry",{}).get("coordinates")[0])
            y = calc_origin_y(orb.get("geometry",{}).get("coordinates")[1])
            orb_file = f'./resources/mapOrbs/{orbFilename}'
            if os.path.exists(orb_file):
                    im=Image.open(orb_file).convert("RGBA")
                    im = im.resize((20,21))
                    map.paste(im,(calc_pixels(x-2),calc_pixels(y-2)),im)

def map_specific_location_orbs(map: Image, name: str):
    
    orbLocationsResponse = requests.get(map_orb_locations)
    orbImageResponse = requests.get(map_orb_image_names)
    orbFilenames = orbImageResponse.json().get("icons")

    for orb in orbLocationsResponse.json()["features"]:
        if orb.get("geometry",{}).get("coordinates")[2] == 0:
            if orb.get("properties",{}).get("icon") == name:
                orbFilename = orbFilenames.get(orb.get("properties",{}).get("icon")).get("filename")
                x = calc_origin_x(orb.get("geometry",{}).get("coordinates")[0])
                y = calc_origin_y(orb.get("geometry",{}).get("coordinates")[1])
                orb_file = f'./resources/mapOrbs/{orbFilename}'
                if os.path.exists(orb_file):
                    im=Image.open(orb_file).convert("RGBA")
                    im = im.resize((20,21))
                    map.paste(im,(calc_pixels(x-2),calc_pixels(y-2)),im)


