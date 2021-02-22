######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################
import os
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import numpy as np
from numpy.lib.type_check import imag

from models.project import Project
from models.class_ import Class_
from models.polygon import Polygon
from models.image_ import Image_

project = Project()

def loadProject():

    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    project.projectDir = filedialog.askdirectory()

    name = project.projectDir.split('/')
    project.name = name[len(name) - 1]
    
    # Debugging placeholder dir [Only for testing]
    #project.projectDir = "/home/pepv/Practiques/Segm/Software/MRI"

    # Load images.sa
    with open(project.projectDir + '/images/images.sa') as f:
        data = json.load(f)

        images = []

        for d in data:
            images.append(Image_(d["srcPath"],d["name"],d["imagePath"],d["thumbPath"]))

        project.images = images

    # Load classes.json
    with open(project.projectDir + '/classes.json') as f:
        data = json.load(f)

        classes = []

        for d in data:
            classes.append(Class_(d["color"],d["id"],d["name"]))
        
        project.classes = classes

    # Load annotations.jason
    with open(project.projectDir + '/annotations.json') as f:
        data = json.load(f)

        # Foreach image
        for i in project.images:

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
                

def createMask(img):
    image = Image.open(img.imagePath)
    back = Image.new('RGB', (image.size[0],image.size[1]), (0, 0, 0))
    draw = ImageDraw.Draw(back)

    for poly in img.polygons:

        # Get hex color and strip '#'
        colorHex = project.classes[poly.classId - 1].color.lstrip('#')
        # Convert hex color to rgb
        colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))

        draw.polygon(poly.points,fill = colorRGB,outline = colorRGB)

    back.save('masks/'+ project.name +'/mask_'+ img.name, quality=100)

def main():
    loadProject()

    if not os.path.isdir("masks/" + project.name):
        os.makedirs("masks/" + project.name)

    for img in project.images:
        createMask(img)

if __name__ == "__main__":
    main()