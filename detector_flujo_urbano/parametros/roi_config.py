def points_roi(video_id):
    #los videos tendrán distinto Id para manejarlos mejor
    xr1 = 0
    xr2 = 0
    yr1 = 0
    yr2 = 0
    #sur oriente arriba-abajo
    if(video_id=='sur_or_ab'):
        xr1 = 1000
        xr2 = 1850
        yr1 = 0
        yr2 = 700
    #sur oriente izquierda derecha
    elif(video_id=='sur_or_id'):
        #VALORES ORIGINALES
        #xr1 = 0
        #xr2 = 1200
        #yr1 = 300
        #yr2 = 1000
        xr1 = 1775
        xr2 = 2375
        yr1 = 1100
        yr2 = 2200
    #nor occidente arriba abajo (estos valores estan obtenidos)
    elif(video_id=='nor_oc_ab'):
        xr1 = 0
        xr2 = 800
        yr1 = 300
        yr2 = 1050
    #nor occidente diagonal (estos valores estan obtenidos)
    elif(video_id=='nor_oc_d'):
        xr1 = 950
        xr2 = 2000
        yr1 = 300
        yr2 = 1050
    #nor oriente izquierda derecha (estos valores estan obtenidos)
    elif(video_id=='nor_or_id'):
        xr1 = 0
        xr2 = 950
        yr1 = 0
        yr2 = 450
    #nor oriente arriba abajo (estos valores estan obtenidos)
    elif(video_id=='nor_or_ab'):
        xr1 = 900
        xr2 = 1850
        yr1 = 350
        yr2 = 1050
    #sur occidente arriba abajo (estos valores estan obtenidos)
    elif(video_id=='sur_oc_ab'):
        xr1 = 0
        xr2 = 500
        yr1 = 0
        yr2 = 700
    #puente guambra izquierda (estos valores estan obtenidos)
    elif(video_id=='p_g_i'):
        xr1 = 0
        xr2 = 1650
        yr1 = 200
        yr2 = 1000
    #puente guambra derecha diagonal (estos valores estan obtenidos)
    elif(video_id=='p_g_d'):
        xr1 = 2800
        xr2 = 4100
        yr1 = 1500
        yr2 = 2200
    #puente guambra arriba abajo (estos valores estan obtenidos)
    elif(video_id=='p_g_ab'):
        xr1 = 1775
        xr2 = 2375
        yr1 = 1100
        yr2 = 2200
   
    return xr1,xr2, yr1, yr2 

def size_roi(video_id,video_size):
    height = 0
    width = 0

    if(video_id=='sur_or_ab'):
        height = video_size[1]//3
        width = video_size[0]//2
    elif(video_id=='sur_or_id'):
        height = video_size[0]//3
        width = video_size[1]//3

    return height,width

def get_exit_points(video_id,shape):
    EXIT_PTS = []
    if(video_id=='sur_or_id'):
        EXIT_PTS = [[(0, 0),(shape[1]//4, shape[0])],
                    [(shape[1]//4*3,0),(shape[1],shape[0])]]
    elif(video_id=='sur_or_ab'):
        EXIT_PTS = [[(0, 0),(shape[1]//4, shape[0])],
                    [(shape[1]//4*3,0),(shape[1],shape[0])],
                    [(0,shape[0]//3*2),(shape[1],shape[0])]]    
    return EXIT_PTS

def get_measurements(video_id):
    measure = {}
    if(video_id=='sur_or_id'):
        measure['wh_heavy_vehicles']={"min_w":150,"max_w":400,"min_h":0,"max_h":1000}
        measure['wh_cars']={"min_w":50,"max_w":149,"min_h":0,"max_h":1000}
        measure['wh_motorcycles']={"min_w":18,"max_w":49,"min_h":0,"max_h":1000}
        measure['wh_people']={"min_w":0,"max_w":17,"min_h":0,"max_h":1000}
    elif(video_id=='sur_or_ab'):
        measure['wh_heavy_vehicles']={"min_w":150,"max_w":400,"min_h":0,"max_h":1000}
        measure['wh_cars']={"min_w":50,"max_w":149,"min_h":0,"max_h":1000}
        measure['wh_motorcycles']={"min_w":18,"max_w":49,"min_h":0,"max_h":1000}
        measure['wh_people']={"min_w":0,"max_w":17,"min_h":0,"max_h":1000}

    return measure
    