import json
import tkinter as tk
from tkinter import filedialog

from models.project import Project
from models.class_ import Class_
from models.point import Point
from models.polygon import Polygon
from models.image import Image

project = Project()

def openFileNameDialog():

    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    project.projectDir = filedialog.askdirectory()
    
    # Debug dir (avoid VScode error with tkinter)
    # project.projectDir = "/home/pepv/Practiques/Segm/Software/Test_json"

    # Load images.sa
    with open(project.projectDir + '/images/images.sa') as f:
        data = json.load(f)

        images = []

        for d in data:
            images.append(Image(d["srcPath"],d["name"],d["imagePath"],d["thumbPath"]))

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
                        points.append(Point(pointArray[k:k + 2]))

                    polygons.append(Polygon(poly["classId"], points))
            
            i.polygons = polygons
                

                
def main():
    openFileNameDialog()

if __name__ == "__main__":
    main()