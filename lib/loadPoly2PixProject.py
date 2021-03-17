import tkinter as tk
from tkinter import filedialog
import os, sys, json
from PIL import Image, ImageDraw

from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

def loadPoly2PixProject():
    prj = Project()
    
    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    project = filedialog.askopenfilename()
    
    # Debugging placeholder dir [Only for testing]
    #project= "/home/pepv/Practiques/Segm/Software/sa_poly2pixel/masks/RM1/project.json"

    with open(project) as f:

        data = json.load(f)

    prj.projectDir = data['projectDir']
    prj.name = data['name']

    images = []

    for img in data['images']:
        polygons = []

        for poly in img['polygons']:
            points = []

            for point in poly['points']: points.append((point['x'],point['y']))
            polygons.append(Polygon(poly['classId'], points))
        
        images.append(Image_(img['srcPath'],img['name'],img['imagePath'], img['thumbPath'], polygons))
    
    prj.images = images
    classes = []

    for cls in data['classes']:
        classes.append(Class_(cls['color'], cls['id'], cls['name']))

    prj.classes = classes
            
    return prj