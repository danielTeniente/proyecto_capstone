
#get center of rectangles
from .get_centroid import get_centroid
from .detect_taxis import detect_taxis

#open CV
import cv2


def detect_vehicles(img, img_color, 
    wh_cars={"min_w":0,"max_w":0,"min_h":0,"max_h":0},
    wh_motorcycles={"min_w":0,"max_w":0,"min_h":0,"max_h":0},
    wh_people={"min_w":0,"max_w":0,"min_h":0,"max_h":0},
    wh_heavy_vehicles={"min_w":0,"max_w":0,"min_h":0,"max_h":0}):

    """
    img: img or frame to detect vehicles
    w h represents width w and height h of 
    the rectangle that surround the vehicle.

    You can stablish a min and max width and height
    for cars, motorcycles, people and heavy vehicles

    by default, it only detects cars
    """

    #dictionary to save all types of vehicles
    vehicles_founded = {"cars":[],
        "motorcycles":[],
        "heavy_vehicles":[],
        "people":[],
        "taxis":[]}

    color_mask = detect_taxis(img_color)

    #find contours of a image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)



    # filtering types of vehicles
    for (i, contour) in enumerate(contours):
        #coordinates of rectángle that surround the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        #boolean information
        # width and height should for cars, motorcycles, heavy_vehicles and people
        is_a_car = (
            w >= wh_cars["min_w"]) and ( 
            h >= wh_cars["min_h"]) and (
            w < wh_cars["max_w"]) and (
            h < wh_cars["max_h"])

        is_a_heavy = (
            w >= wh_heavy_vehicles["min_w"]) and ( 
            h >= wh_heavy_vehicles["min_h"]) and (
            w < wh_heavy_vehicles["max_w"]) and (
            h < wh_heavy_vehicles["max_h"])

        is_a_person = (
            w >= wh_people["min_w"]) and ( 
            h >= wh_people["min_h"]) and (
            w < wh_people["max_w"]) and (
            h < wh_people["max_h"])
            
        is_a_motorcycle = (
            w >= wh_motorcycles["min_w"]) and ( 
            h >= wh_motorcycles["min_h"]) and (
            w < wh_motorcycles["max_w"]) and (
            h < wh_motorcycles["max_h"])

        if is_a_car:       
            # getting center of the bounding box
            centroid = get_centroid(x, y, w, h)
            #cv2.rectangle(color_mask, (x,y), (x+w,y+h), 255, 3)
            
            is_a_taxi = (color_mask[y:y+h,x:x+w].sum()>0) 

            if is_a_taxi:
                vehicles_founded["taxis"].append(((x, y, w, h), centroid))
            else:
            #save the rectangle and the center of it
                vehicles_founded["cars"].append(((x, y, w, h), centroid))

        if is_a_heavy:
            #getting center of the bounding box
            centroid = get_centroid(x, y, w, h)

            vehicles_founded["heavy_vehicles"].append(((x, y, w, h), centroid))

        if is_a_motorcycle:
            #getting center of the bounding box
            centroid = get_centroid(x, y, w, h)

            vehicles_founded["motorcycles"].append(((x, y, w, h), centroid))

        if is_a_person:
            #getting center of the bounding box
            centroid = get_centroid(x, y, w, h)

            vehicles_founded["people"].append(((x, y, w, h), centroid))

        #cv2.imshow('Taxis',color_mask)
    return vehicles_founded