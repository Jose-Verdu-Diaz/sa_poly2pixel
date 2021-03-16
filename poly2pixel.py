######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################
import os, sys, json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

from models.project import Project
from models.class_ import Class_
from models.polygon import Polygon
from models.image_ import Image_

project = None

# Show file browser and load SuperAnnotate project (create project object)
def loadProject():

    prj = Project()

    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    prj.projectDir = filedialog.askdirectory()

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

# Show file browser and load SuperAnnotate exported project (create project object)
def loadExportedProject():

    prj = Project()
    
    # Directory explorer
    root = tk.Tk()
    root.withdraw()

    prj.projectDir = filedialog.askdirectory()
    
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
            
            _images.append(Image_(None,f.strip('.json'),prj.projectDir + '/img/' + f.strip('.json') + '.jpg', None, polygons))               
    prj.images = _images

    # Load classes.json
    with open(prj.projectDir + '/classes.json') as f:
        data = json.load(f)

        classes = []

        for d in data:
            classes.append(Class_(d["color"],d["id"],d["name"]))
        
        prj.classes = classes
        
    return prj

# Create image masks from the project object
def createMask(prj):

    for img in prj.images:

        image = Image.open(img.imagePath)
        back = Image.new('RGB', (image.size[0],image.size[1]), (0, 0, 0))
        draw = ImageDraw.Draw(back)

        for poly in img.polygons:

            # Get hex color and strip '#'
            colorHex = prj.classes[poly.classId - 1].color.lstrip('#')
            # Convert hex color to rgb
            colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))

            draw.polygon(poly.points,fill = colorRGB,outline = colorRGB)

        back.save('masks/'+ prj.name +'/img/mask_'+ img.name + '.bmp', quality=100, subsampling=0)

# Create a json file from projec object
def createProjectJson(prj):
    projectJson = {'projectDir' : prj.projectDir, 'name' : prj.name, 'images' : [] , 'classes' : []}

    # Foreach image
    for img in prj.images:

        # Foreach polygon of the image
        polygonsJson = []
        for poly in img.polygons:

            # Foreach point of the polygon
            points = []
            for point in poly.points:
                points.append({'x' : point[0], 'y' : point[1]})

            polygonsJson.append({'classId' : poly.classId, 'points' : points})

        # Add images to json
        projectJson['images'].append({ 'srcPath' : img.srcPath, 'name' : img.name, 'imagePath' : img.imagePath, 'thumbPath' : img.thumbPath, 'polygons' : polygonsJson}) 

    # Foreach class
    for class_ in prj.classes:
        projectJson['classes'].append({ 'id' : class_.id, 'color' : class_.color, 'name' : class_.name}) 


    with open('masks/'+ prj.name + '/project.json', 'w', encoding='utf-8') as f:
        json.dump(projectJson, f, ensure_ascii=False, indent=4)

def main():

    option = input('(1) Import SA project\n(2) Import exported SA project\n')

    # Load project
    if option == '1':
        project = loadProject()
    elif option == '2':
        project = loadExportedProject()
    else:
        print('Unexpected option')
        sys.exit()

    # Create project dir
    if not os.path.isdir('masks/' + project.name):
        os.makedirs('masks/' + project.name + '/img')

    # Create masks
    createMask(project)
    
    # Create project json
    createProjectJson(project)

if __name__ == "__main__":
    main()