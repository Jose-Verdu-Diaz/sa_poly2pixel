import os, sys, json
from PIL import Image, ImageDraw

from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

# Create image masks from the project object
def createMask(prj):
    # Create project dir
    if not os.path.isdir('masks/' + prj.name):
        os.makedirs('masks/' + prj.name + '/img')
        
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
