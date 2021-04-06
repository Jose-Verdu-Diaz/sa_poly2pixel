import tkinter as tk
from tkinter import filedialog
import os, sys, json
from PIL import Image, ImageDraw

from lib.aux import *
from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

# Show file browser and load SuperAnnotate exported project (create project object)
def loadExportedProject():

    prj = Project()
    
    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    prj.projectDir = filedialog.askdirectory()

    if not isinstance(prj.projectDir, str) or prj.projectDir == '': 
        input(f'\n{bcolors.FAIL}No project selected, press a key to continue...{bcolors.ENDC}')
        return  

    # Debugging placeholder dir [Only for testing]
    #prj.projectDir = "/home/pepv/Practiques/Segm/MRIs/Tracked/RM1"

    name = prj.projectDir.split('/')
    prj.name = name[len(name) - 1]

    maskFiles = sorted(os.listdir(prj.projectDir + '/annotations'))
    imageFiles = sorted(os.listdir(prj.projectDir + '/img'))
    classFile = prj.projectDir + 'classes.json'

    _images = []



    #if f.strip('.json') in [i.strip('.jpg') for i in imageFiles] :

    for f in maskFiles:

        with open(prj.projectDir + '/annotations/' + f) as m:

            data = json.load(m)

            polygons = []

            # Foreach polygon
            for poly in data['instances']:
                pointArray = poly['points']
                points = []
                # Group points in pairs
                for k in range(0, len(pointArray), 2):
                    points.append((pointArray[k],pointArray[k + 1]))

                polygons.append(Polygon(poly['classId'], points))
            
            _images.append(Image_(None,f.strip('.json').strip('.jpg'),prj.projectDir + '/img/' + f.strip('.json'), None, polygons))               
    prj.images = _images

    # Load classes.json
    with open(prj.projectDir + '/classes.json') as f:
        data = json.load(f)

        classes = []

        for d in data:
            classes.append(Class_(d["color"],d["id"],d["name"]))
        
        prj.classes = classes
        
    return prj
