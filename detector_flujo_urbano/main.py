

from funciones.detect_vehicles import detect_vehicles
from parametros.roi_config import *

import numpy as np
import cv2
import argparse
import math

#se envía la ubicación del vehículo y se pregunta si está o no en la zona de salida
def check_exit(point, exit_masks):
    for exit_mask in exit_masks:
        try:
            # (y,x)
            if exit_mask[point[1]][point[0]][0] == 255:
                return True
        except:
            return True
    return False

def train_bg_subtractor(inst, cap, num=500):
    '''
        BG substractor need process some amount of frames to start giving result
    '''
    print ('Training BG Subtractor...')

    for i in range(num):
        ret, frame = capture.read()
        inst.apply(frame, None, 0.0025)


def distance(x, y, x_weight=1.0, y_weight=1.0):

    return math.sqrt(float((x[0] - y[0])**2) / x_weight + float((x[1] - y[1])**2) / y_weight)        
        


def draw_count(img, num_autos=0,num_buses=0,num_motos=0,num_personas=0, num_taxis=0):      

    # drawing top block with counts
    cv2.rectangle(img, (0, 0), (img.shape[1], 50), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, ("Ligeros: {n_a}, Pesados: {n_b}, Personas: {n_c}, Motocicletas: {n_d}, Taxis:{n_e}".format(n_a=num_autos,
    n_b=num_buses,
    n_c=num_personas,
    n_d=num_motos,
    n_e=num_taxis)), (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return img

def contar_vehiculos(pathes=[],matches=[],path_size=10,exit_masks=None,vehicle_count=0):
    #######################################
    # SEGUIMIENTO DEL VEHÍCULO 
    #######################################
    # se verifica si el path del vehículo ya existe
    if not pathes:
        for match in matches:
            pathes.append([match[1]])
    else:
        # link new matches with old pathes based on minimum distance between
        # matches
        new_pathes = []
        for path in pathes:
            _min = 999999
            _match = None
            for vehiculo in matches:
                if len(path) == 1:
                    #comparo la distancia de los centros que hay en los rectángulos
                    d = distance(vehiculo[1], path[-1])
                else:
                    # based on 2 prev matches predict next point and calculate
                    # distance from predicted next point to current
                    xn = 2 * path[-1][0] - path[-2][0]
                    yn = 2 * path[-1][1] - path[-2][1]
                    #Mira la distancia entre el primer punto y el segundo
                    d = distance(
                        vehiculo[1], (xn, yn),
                        x_weight=x_weight,
                        y_weight=y_weight
                    )

                #distancia mínima para poder predecir los siguientes puntos
                if d < _min:
                    _min = d
                    _match = vehiculo

            #si match se setea
            if _match and _min <= max_dst:
                matches.remove(_match)
                path.append(_match[1])
                new_pathes.append(path)

            # do not drop path if current frame has no matches
            if _match is None:
                new_pathes.append(path)

        pathes = new_pathes

        # add new pathes
        if len(matches):
            for vehiculo in matches:
                # do not add matches that already should be counted
                if check_exit(vehiculo[1],exit_masks):
                    continue
                pathes.append([vehiculo[1]])

    # save only last N matches in path
    for i in range(len(pathes)):
        pathes[i] = pathes[i][path_size * -1:]


    ################################################
    #CONTEO
    ###############################################
    # count vehicles and drop counted pathes:
    new_pathes = []
    for i, path in enumerate(pathes):
        d = path[-2:]

        if (
            # need at list two matches to count
            len(d) >= 2 and
            # prev point not in exit zone
            not check_exit(d[0],exit_masks) and
            # current point in exit zone
            check_exit(d[1],exit_masks) and
            # path len is bigger than min
            path_size <= len(path)
        ):
            vehicle_count += 1
        else:
            # prevent linking with path that already in exit zone
            add = True
            for vehiculo in path:
                if check_exit(vehiculo,exit_masks):
                    add = False
                    break
            if add:
                new_pathes.append(path)

    pathes = new_pathes

    return vehicle_count,pathes
    



###############################
#FUNCIÓN PRINCIPAL
###############################

parser = argparse.ArgumentParser(description='This program uses OpenCv to count vehicles')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--config', type=str, help='Configurations for proccessing video: sur_or_ab, sur_or_id, nor_or,nor_oc', default='sur_or_id')

args = parser.parse_args()
#backSub = cv2.createBackgroundSubtractorKNN()
#history toma en cuenta cuántos frames anteiores se usan para considerar lo que es el fondo
#si un objeto aparece en la misma posisicón durante los mismos frames que el history, el objeto
#es tomado como fondo
backSub = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)


capture = cv2.VideoCapture(cv2.samples.findFileOrKeep(args.input))

if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)

# skipping 500 frames to train bg subtractor
#train_bg_subtractor(backSub, capture, num=499)

ret, frame = capture.read()
height , width , layers =  frame.shape
new_h, new_w = size_roi(args.config,(height , width))
SHAPE = (new_h,new_w)


EXIT_PTS = get_exit_points(args.config,SHAPE)

exit_mask = np.zeros(SHAPE + (3,), dtype='uint8')

#se dibujan rectángulos para marcar la zona de salida
for rectangles in EXIT_PTS:
    cv2.rectangle(exit_mask, rectangles[0], rectangles[1], (255,255,255), -1)

#Esta lista servirá para darle seguimiento a los vehículos
pathes_autos = []
pathes_buses = []
pathes_personas = []
pathes_motos = []
pathes_taxis = []

#pesos considerados para la medición de la distancia
x_weight = 1
y_weight = 50.

max_dst=50
path_size=7

#contadores
contador_autos = 0
contador_pesados = 0
contador_motos = 0
contador_personas = 0
contador_taxis = 0

##################################33
#Procesamiento del video
###############################33

while True:

    ret, frame = capture.read()
    if frame is None:

        break
    ###################################
    #REGIÓN DE INTERES roi
    ####################################
    xr1, xr2, yr1, yr2 = points_roi(video_id=args.config)
    roi = frame[yr1:yr2,xr1:xr2]
    cv2.rectangle(frame,(xr1,yr1),(xr2,yr2),(255,0,0),thickness=10)

    ###################################
    #Eliminación del fondo y filtros
    ###################################
    fgMask = cv2.GaussianBlur(roi, (5, 5), 0)
    
    fgMask = backSub.apply(fgMask,None, 0.003)


    #filtros
    #menores a 5,5 produce muchos bordes
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 7))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Remove noise
    opening = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel_close)

    # Fill any small holes
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # Dilate to merge adjacent blobs
    dilation = cv2.dilate(closing, kernel, iterations=3)

    # threshold
    dilation[dilation < 250] = 0


    ###############################################
    #CAMBIO DE TAMAÑO DE LA IMAGEN
    ###############################################
    resized_frame = cv2.resize(frame, (width//3, height//3)) 
    resized_roi = cv2.resize(roi, (new_w, new_h)) 
    resized_fgMask = cv2.resize(dilation, (new_w, new_h)) 
    #cv2.imshow('ROI', resized_roi)


    ###############################################
    # DETECCIÓN DE VEHÍCULOS
    ########################################

    #Se buscan VEHICULOS en la imaen
    # estas medidas sirvan para viaje en el eje x
    medidas = get_measurements(args.config)
    matches = detect_vehicles(resized_fgMask, resized_roi,
        wh_heavy_vehicles=medidas['wh_heavy_vehicles'],
        wh_cars=medidas['wh_cars'],
        wh_motorcycles=medidas['wh_motorcycles'],
        wh_people=medidas['wh_people'])

    #se dibujan rectángulos cuando encuentra un vehículo
    for match in matches["cars"]:
        (x, y, w, h) = match[0]
        #dibuja un rectángulo
        if(check_exit(match[1],[exit_mask])):
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (0, 128, 0), 3)
        else:
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (173, 255, 47), 3)

    for match in matches["taxis"]:
        (x, y, w, h) = match[0]
        #dibuja un rectángulo
        if(check_exit(match[1],[exit_mask])):
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (99, 156, 156), 3)
        else:
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (23, 255, 252), 3)

    #se dibujan rectángulos cuando encuentra un vehículo pesado
    for match in matches["heavy_vehicles"]:
        (x, y, w, h) = match[0]
        #dibuja un rectángulo
        if(check_exit(match[1],[exit_mask])):
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (75, 0, 130), 3)
        else:
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (255, 105, 180), 3) 

    #se dibujan rectángulos cuando encuentra un moto
    for match in matches["motorcycles"]:
        (x, y, w, h) = match[0]
        #dibuja un rectángulo
        if(check_exit(match[1],[exit_mask])):
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (155, 85, 161), 3)
        else:
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (182, 15, 206), 3)            
   
    #se dibujan rectángulos cuando encuentra una persona
    for match in matches["people"]:
        (x, y, w, h) = match[0]
        #dibuja un rectángulo
        if(check_exit(match[1],[exit_mask])):
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (46, 26, 136), 3)
        else:
            cv2.rectangle(resized_roi, (x,y), (x+w,y+h), (108, 79, 237), 3)            
        

    ###############################################
    #  VISUALIZACIÓN DE ROI Y EXIT ZONE
    #########################################

    #Se reproduce la imagen completa
    cv2.imshow('Last Frame',resized_frame)

    #se superpone la máscara de exit zone para poder detectar el flujo vehiculas
    cv2.addWeighted(exit_mask, 0.1, resized_roi, 0.9, 0, resized_roi)
    #############33
    #Dibuja el contador
    ########################33
    draw_count(resized_roi,
        num_autos=contador_autos,
        num_buses=contador_pesados,
        num_motos=contador_motos,
        num_personas=contador_personas,
        num_taxis=contador_taxis)   
    #se reproduce la imagen zoom de la zona evaluada
    cv2.imshow('Frame', resized_roi)
    #se muestra la máscara sin fondo
    #cv2.imshow('FG Mask', resized_fgMask)
    exit_masks = [exit_mask]
    contador_autos,pathes_autos = contar_vehiculos(pathes=pathes_autos,matches=matches["cars"],path_size=path_size,exit_masks=exit_masks,vehicle_count=contador_autos)
    contador_pesados,pathes_buses = contar_vehiculos(pathes=pathes_buses,matches=matches["heavy_vehicles"],path_size=path_size,exit_masks=exit_masks,vehicle_count=contador_pesados)
    contador_motos,pathes_motos = contar_vehiculos(pathes=pathes_motos,matches=matches["motorcycles"],path_size=path_size,exit_masks=exit_masks,vehicle_count=contador_motos)
    contador_personas,pathes_personas = contar_vehiculos(pathes=pathes_personas,matches=matches["people"],path_size=path_size,exit_masks=exit_masks,vehicle_count=contador_personas)
    contador_taxis,pathes_taxis = contar_vehiculos(pathes=pathes_taxis,matches=matches["taxis"],path_size=path_size,exit_masks=exit_masks,vehicle_count=contador_taxis)

    #cerrar el programa
    keyboard = cv2.waitKey(30)

    if keyboard == 'q' or keyboard == 27:
        break    
