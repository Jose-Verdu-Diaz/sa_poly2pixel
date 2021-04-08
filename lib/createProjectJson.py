import os, sys, json
from PIL import Image, ImageDraw

from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

# Create a json file from projec object
def createProjectJson(prj):

    if not os.path.exists(f'projects/{prj.name}'):
        os.makedirs(f'projects/{prj.name}')

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


    with open('projects/'+ prj.name + '/project.json', 'w', encoding='utf-8') as f:
        json.dump(projectJson, f, ensure_ascii=False, indent=4)
