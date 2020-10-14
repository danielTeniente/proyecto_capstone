#open CV
import cv2

def detect_vehicles(img, 
    wh_cars={"min_w":18,"max_w":150,"min_h":18,"max_h":120},
    wh_motorcycles={"min_w":0,"max_w":0,"min_h":0,"max_h":0},
    wh_people={"min_w":0,"max_w":0,"min_h":0,"max_h":0},
    wh_heavy_vehicles={"min_w":0,"max_w":0,"min_h":0,"max_h":0}):

    """
    img: img or frame to detect vehicles
    w h represents width w and height h of 
    the rectangle that surround the vehicle.

    You can stablish a min and max width and height
    """

    #dictionary to save all types of vehicles
    matches = {"cars":[],
        "motorcycles":[],
        "heavy_vehicles":[],
        "people":[]}

    #find contours of a image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # filtering types of vehicles
    for (i, contour) in enumerate(contours):
        #coordinates of rectángle that surround the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        #boolean information
        # width and height should for cars, motorcycles, heavy_vehicles and people
        is_a_car = (w >= wh_cars["min_w"]) and ( 
            h >= wh_cars["min_h"]) and (
                w < wh_cars["max_w"]) and (
                    h < wh_cars["max_h"])

        is_a_heavy = (w >= wh_heavy_vehicles["min_w"]) and ( 
            h >= wh_heavy_vehicles["min_h"]) and (
                w <= wh_heavy_vehicles["max_w"]) and (
                    h <= wh_heavy_vehicles["max_h"])

        if is_a_car:       
            # getting center of the bounding box
            centroid = get_centroid(x, y, w, h)

            #se almacenan los datos del rectángulo y el centro del rectángulo
            #este rectángulo está relacionado con los contornos encontrados por opencv
            matches["cars"].append(((x, y, w, h), centroid))

        if is_a_heavy:
                    # getting center of the bounding box
            centroid = get_centroid(x, y, w, h)

            #se almacenan los datos del rectángulo y el centro del rectángulo
            #este rectángulo está relacionado con los contornos encontrados por opencv
            matches["heavy_vehicles"].append(((x, y, w, h), centroid))

    return matche