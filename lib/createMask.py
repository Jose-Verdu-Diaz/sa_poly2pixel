import os, cv2, json
from PIL import Image, ImageDraw
import numpy as np

from lib.auxiliary import *
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
            ┃ 3 : Individual masks  ┃
            ┃ 4 : Binary masks      ┃
            ┃ 5 : Mono masks        ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Create project dir
        if not os.path.isdir('projects/' + prj.name + '/masks'):
            os.makedirs('projects/' + prj.name + '/masks')

        if choice == '0':
            return   

        elif choice == '1':
            if not os.path.exists(f'projects/{prj.name}/img'):
                input(f'\n{bcolors.FAIL}Import images first. Continue...{bcolors.ENDC}')
                return

            if not os.path.exists(f'projects/{prj.name}/masks'):
                os.makedirs(f'projects/{prj.name}/masks')

            # Only 255 supported classes. Check project.
            if len(prj.classes) >= 255:
                input(f'\n{bcolors.FAIL}Only 255 classes supported in Black and White.\nThere are {len(prj.classes)}, press a key to continue...{bcolors.ENDC}')
                return

            for img in prj.images:
                image = Image.open(f'projects/{prj.name}/img/{img.name}.jpg')
                back = Image.new('L', (image.size[0],image.size[1]))
                draw = ImageDraw.Draw(back)

                for poly in img.polygons:
                    draw.polygon(poly.points,fill = int(poly.classId),outline = int(poly.classId))

                back.save(f'projects/{prj.name}/masks/{img.name}.bmp', quality=100, subsampling=0)

            input(f'\n{bcolors.OKGREEN}Black and White masks created, press a key to continue...{bcolors.ENDC}')

        elif choice == '2':
            if not os.path.exists(f'projects/{prj.name}/img'):
                input(f'\n{bcolors.FAIL}Import images first. Continue...{bcolors.ENDC}')
                return

            if not os.path.exists(f'projects/{prj.name}/masks_color'):
                os.makedirs(f'projects/{prj.name}/masks_color')

            for img in prj.images:

                image = Image.open(f'projects/{prj.name}/img/{img.name}.jpg')
                back = Image.new('RGB', (image.size[0],image.size[1]), (0, 0, 0))
                draw = ImageDraw.Draw(back)

                for poly in img.polygons:

                    # Get hex color and strip '#'
                    colorHex = prj.classes[poly.classId - 1].color.lstrip('#')
                    # Convert hex color to rgb
                    colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))

                    draw.polygon(poly.points,fill = colorRGB,outline = colorRGB)

                back.save(f'projects/{prj.name}/masks_color/{img.name}.bmp', quality=100, subsampling=0)

            input(f'\n{bcolors.OKGREEN}Color masks created, press a key to continue...{bcolors.ENDC}')
        
        elif choice == '3':
            if not os.path.exists(f'projects/{prj.name}/masks'):
                input(f'\n{bcolors.FAIL}Create B&W masks first. Continue...{bcolors.ENDC}')
                return

            ims = []
            files=[]
            for file in sorted(os.listdir(f'projects/{prj.name}/masks')):
                ims.append(cv2.imread(f'projects/{prj.name}/masks/{file}'))
                files.append(os.path.splitext(file)[0])

            printProgressBar(0, len(prj.classes)*len(ims), prefix = 'Extracting individual masks:', suffix = 'Complete', length = 50)

            if not os.path.exists(f'projects/{prj.name}/individual'):
                os.makedirs(f'projects/{prj.name}/individual')

            for i,cls in enumerate(prj.classes):
                if not os.path.exists(f'projects/{prj.name}/individual/{str(cls.id).zfill(4)}'):
                    os.makedirs(f'projects/{prj.name}/individual/{str(cls.id).zfill(4)}')

                ims_copy = []
                for img in ims:
                    ims_copy.append(img.copy())

                for j,img in enumerate(ims_copy):
                    black_pixels_mask = np.all(img != [cls.id, cls.id, cls.id], axis=-1)
                    non_black_pixels_mask = ~black_pixels_mask

                    img[black_pixels_mask] = [0, 0, 0]
                    img[non_black_pixels_mask] = [255, 255, 255]

                    cv2.imwrite(f'projects/{prj.name}/individual/{str(cls.id).zfill(4)}/{files[j]}_{str(cls.id).zfill(4)}.bmp', img)
                
                    printProgressBar(i*len(ims) + j, len(prj.classes)*len(ims), prefix = 'Extracting individual masks:', suffix = f'({i*len(ims) + j}/{len(prj.classes)*len(ims)})', length = 50)

        # Binary masks
        elif choice == '4':
            if not os.path.exists(f'projects/{prj.name}/img'):
                input(f'\n{bcolors.FAIL}Import images first. Continue...{bcolors.ENDC}')
                return

            if not os.path.exists(f'projects/{prj.name}/binary_masks'):
                os.makedirs(f'projects/{prj.name}/binary_masks')

            for img in prj.images:
                image = Image.open(f'projects/{prj.name}/img/{img.name}.jpg')
                back = Image.new('L', (image.size[0],image.size[1]))
                draw = ImageDraw.Draw(back)

                for poly in img.polygons:
                    draw.polygon(poly.points,fill = int(255),outline = int(255))

                back.save(f'projects/{prj.name}/binary_masks/{img.name}.bmp', quality=100, subsampling=0)

            input(f'\n{bcolors.OKGREEN}Binary masks created, press a key to continue...{bcolors.ENDC}')

        elif choice == '5':

            mono_classFile = prj.projectDir + '/classes_mono.json'

            with open(mono_classFile) as f:
                data = json.load(f)
                classes = []

                for d in data: classes.append(Class_(d["color"],d["id"],d["name"]))

            if not os.path.exists(f'projects/{prj.name}/img'):
                input(f'\n{bcolors.FAIL}Import images first. Continue...{bcolors.ENDC}')
                return

            if not os.path.exists(f'projects/{prj.name}/mono_masks'):
                os.makedirs(f'projects/{prj.name}/mono_masks')

            # Only 255 supported classes. Check project.
            if len(prj.classes) >= 255:
                input(f'\n{bcolors.FAIL}Only 255 classes supported in Black and White.\nThere are {len(prj.classes)}, press a key to continue...{bcolors.ENDC}')
                return

            for img in prj.images:
                image = Image.open(f'projects/{prj.name}/img/{img.name}.jpg')
                back = Image.new('L', (image.size[0],image.size[1]))
                draw = ImageDraw.Draw(back)

                for poly in img.polygons:

                    name = prj.classes[int(poly.classId) - 1].name
                    search = name.replace('_L','').replace('_R','')
                    color = next((cls.id for cls in classes if cls.name == search), None)
                    
                    if color == None: print(name)

                    draw.polygon(poly.points,fill = color,outline = color)

                back.save(f'projects/{prj.name}/mono_masks/{img.name}.bmp', quality=100, subsampling=0)

            input(f'\n{bcolors.OKGREEN}Black and White mono masks created, press a key to continue...{bcolors.ENDC}')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')
