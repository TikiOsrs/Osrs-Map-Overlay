#! /usr/local/bin/python3
from find_objects import *
from find_spawns import *
from plot_map import *
import argparse

if __name__ == "__main__":
    Image.MAX_IMAGE_PIXELS = None
    map_start_x = 18
    map_stary_y = 19
    image_origin_x = 18
    image_origin_y = 196

    object_data, morph_data = pull_object_data()
    map = Image.open('./resources/momo-noOrbs.png')
    overlay = Image.new("RGBA",map.size)
    draw = ImageDraw.Draw(overlay)
    

    parser = argparse.ArgumentParser(description='Input a type, and search-type, along with a query.')
    parser.add_argument('--type', type=str, required=True,
                    help='Pick between \'spawn\' or \'object\'.')
    parser.add_argument('--search-type', type=str, required=False, default="substring", 
                    help='Choose between \'regex\', \'substring\' or \'id\'')
    parser.add_argument('query')
                    

    args = parser.parse_args()
    if args.type.lower() not in ["spawn", "object"]:
        print(f'{args.type} is not a valid choice for --type.')
        print('Pick between \'spawn\' or \'object\'.')
        quit()
    
    if args.search_type.lower() not in ["regex", "substring", "id"]:
        print(f'{args.type} is not a valid choice for --search-type.')
        print('Choose between \'regex\', \'substring\' or \'id\'')
        quit()

    
    if args.type.lower() == "spawn":
        results = spawn_single_lookup(args.query)
        for result in results:
            spawn_draw_location(result,draw,(255,0,0),False)
    
    if args.type.lower() == "object":
        #if substring flag
        if args.search_type == "substring":
            results = object_search_by_substring(args.query, object_data, morph_data)
        #if regex flag
        if args.search_type == "regex":
            results = object_search_by_regex(args.query, object_data, morph_data)
        #if objectid flag
        if args.search_type == "id": 
            results = object_search_by_id(args.query, object_data, morph_data)
        #map it
        for result in results:
            print(results)
            object_draw_location(result,draw,(0,255,0))

    overlay.save(f"output/map-{args.query}.png")


