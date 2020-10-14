def get_centroid(x, y, w, h):
    """ 
    Get the center (cx,cy) of a rectangle.
    (x,y) are the top-left coordinate 
    width w and height h of the rectangle
    
    """
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)