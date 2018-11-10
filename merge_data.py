from get_bounding_boxes import get_bounding_boxes 
import numpy as np
import math
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
import statistics as st

## Given: 
## lats and lons of query area
## image 
## building nodes 

## bb_coord = [lat_min, lon_min, lat_max, lon_max]

def OSM_to_pixels(bb_coord, image_size, buildings, YOLO=True):
    ## bb_area: [lat_min, lon_min, lat_max, lon_max]
    ## image_size: image.size
    ## buildings: OSM fetched data 

    lat_min, lon_min, lat_max, lon_max = bb_coord[0], bb_coord[1], bb_coord[2], bb_coord[3]
    
    ## Define total lat and lon in area 
    width = lon_max-lon_min
    height = lat_max-lat_min
    bb_pixels = []

    if (not YOLO):
    ## All bounding box pixels
        for building in buildings: 
            ## Pixels for a single building
            pixels = []
            for vertex in building: 
                ## vertex is a set (lat, lon)
                lat = vertex[0]
                lon = vertex[1]
                
                ## want each element of pixels to be (pixel x, pixel y)
                pixel_x = math.floor(((lon-lon_min)/width)*image_size[0])
                pixel_y = math.floor(((lat-lat_min)/height)*image_size[1])
                pixels.append((pixel_x, pixel_y))
                
                # End for loop
                
            bb_pixels.append(pixels)
            
            # End for loop
    else :
        # width_min = []
        # height_min = []
        for building in buildings: 
            ## Pixels for a single building
            pixels = []
            lonX = building[0]
            latY = building[1]

            centreX = math.floor(((lonX-lon_min)/width)*image_size[0])
            centreY = math.floor(((latY-lat_min)/height)*image_size[1]) + 10

            # This will break visualize.py
            centreX = (centreX%38)/38
            centreY = (centreY%38)/38
            
            widthPixel = math.floor((building[2]/width)*image_size[0])
            heightPixel = math.floor((building[3]/height)*image_size[1])

            # width_min.append(widthPixel) 
            # height_min.append(heightPixel)

            pixels = [centreX,centreY,widthPixel,heightPixel]
            bb_pixels.append(pixels)
        
        # print('min width is {} and min height is {}'.format(min(width_min), min(height_min)))
        # print('median width is {} and median height is {}'.format(st.median(width_min), st.median(height_min)))

    return bb_pixels

# white_plain_buildings = get_bounding_boxes(41.014456, -73.769573, 41.018465,-73.765043)
# OSM_to_pixels([41.014456, -73.769573, 41.018465,-73.765043],[100,100],white_plain_buildings)

## TODO: Convert Access_Pairs to a function, Filter OSM data for data outside the box.