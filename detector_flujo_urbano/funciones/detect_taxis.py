#open CV
import cv2
import numpy as np

#get center of rectangles
from .get_centroid import get_centroid

def detect_taxis(img):
    
    #hay que encontrar los valores para detectar amarillo
    lower = np.array([20, 60, 60])  
    upper = np.array([40, 255, 255])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv,lower,upper)
    return color_mask
    #contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
