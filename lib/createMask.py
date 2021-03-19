import os, sys, json
from PIL import Image, ImageDraw

from lib.aux import *
from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

# Create image masks from the project object
def createMask(prj):

    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'''
                {bcolors.BOLD}Name:{bcolors.ENDC} {prj.name}
            {bcolors.BOLD}Directory:{bcolors.ENDC} {prj.projectDir}
        {bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}
        {bcolors.BOLD}Nº of classes:{bcolors.ENDC} {len(prj.classes)}
        ''')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Black and white   ┃
            ┃ 2 : Default colors    ┃
            ┃                       ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Create project dir
        if not os.path.isdir('masks/' + prj.name):
            os.makedirs('masks/' + prj.name + '/img')

        if choice == '0':
            return   

        elif choice == '1':

            # Only 255 supported classes. Check project.
            if len(prj.classes) >= 255:
                input(f'\n{bcolors.FAIL}Only 255 classes supported in Black and White.\nThere are {len(prj.classes)}, press a key to continue...{bcolors.ENDC}')
                return

            for img in prj.images:

                image = Image.open(img.imagePath)
                back = Image.new('L', (image.size[0],image.size[1]))
                draw = ImageDraw.Draw(back)

                for poly in img.polygons:
                    draw.polygon(poly.points,fill = int(poly.classId),outline = int(poly.classId))

                back.save('masks/'+ prj.name +'/img/mask_'+ img.name + '.bmp', quality=100, subsampling=0)

            input(f'\n{bcolors.OKGREEN}Black and White masks created, press a key to continue...{bcolors.ENDC}')

        elif choice == '2':
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

            input(f'\n{bcolors.OKGREEN}Color masks created, press a key to continue...{bcolors.ENDC}')
