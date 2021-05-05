import tkinter as tk
from tkinter import filedialog
import json

from lib.aux import *
from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

# Show file browser and load SuperAnnotate project (create project object)
def loadProject():

    prj = Project()

    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    prj.projectDir = filedialog.askdirectory()

    if not isinstance(prj.projectDir, str) or prj.projectDir == '': 
        input(f'\n{bcolors.FAIL}No project selected, press a key to continue...{bcolors.ENDC}')
        return

    name = prj.projectDir.split('/')
    prj.name = name[len(name) - 1]
    
    # Debugging placeholder dir [Only for testing]
    #prj.projectDir = "/home/pepv/Practiques/Segm/Software/MRI"

    # Load images.sa
    with open(prj.projectDir + '/images/images.sa') as f:
        data = json.load(f)

        images = []

        for d in data:
            images.append(Image_(d["srcPath"],d["name"],d["imagePath"],d["thumbPath"]))

        prj.images = images

    # Load classes.json
    with open(prj.projectDir + '/classes.json') as f:
        data = json.load(f)

        classes = []

        for d in data:
            classes.append(Class_(d["color"],d["id"],d["name"]))
        
        prj.classes = classes

    # Load annotations.jason
    with open(prj.projectDir + '/annotations.json') as f:
        data = json.load(f)

        # Foreach image
        for i in prj.images:

            # If image present on annotations.jason
            if i.name in data:

                polygons = []

                # Foreach polygon
                for poly in data[i.name]["instances"]:
                    pointArray = poly["points"]
                    points = []
                    # Group points in pairs
                    for k in range(0, len(pointArray), 2):
                        points.append((pointArray[k],pointArray[k + 1]))

                    polygons.append(Polygon(poly["classId"], points))
            
            i.polygons = polygons

    return prj             
