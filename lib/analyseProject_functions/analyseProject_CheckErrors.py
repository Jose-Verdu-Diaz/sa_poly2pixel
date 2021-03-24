import os, sys, cv2
import numpy as np

from lib.aux import *
from lib.showSequence import *
from lib.aux import *


def ap_checkErrors(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Search class errors ┃
            ┃                         ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            '''
            img = cv2.imread('test19.bmp',cv2.IMREAD_GRAYSCALE)
            contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            input(len(contours))
            '''
            dir = '/home/pepv/Practiques/Segm/Software/sa_poly2pixel/masks/RM1/img'
            ims = []
            for file in sorted(os.listdir(dir)):
                ims.append(cv2.imread(f'{dir}/{file}'))

            printProgressBar(0, len(prj.classes)*len(ims), prefix = 'Extracting individual masks:', suffix = 'Complete', length = 50)

            if not os.path.exists(f'masks/{prj.name}/individual'):
                os.makedirs(f'masks/{prj.name}/individual')

            for i,cls in enumerate(prj.classes):
                if not os.path.exists(f'masks/{prj.name}/individual/{cls.id}_{cls.name}'):
                    os.makedirs(f'masks/{prj.name}/individual/{cls.id}_{cls.name}')

                ims_copy = []
                for img in ims:
                    ims_copy.append(img.copy())

                for j,img in enumerate(ims_copy):
                    black_pixels_mask = np.all(img != [cls.id, cls.id, cls.id], axis=-1)
                    non_black_pixels_mask = ~black_pixels_mask

                    img[black_pixels_mask] = [0, 0, 0]
                    img[non_black_pixels_mask] = [255, 255, 255]

                    cv2.imwrite(f'masks/{prj.name}/individual/{cls.id}_{cls.name}/{j}.bmp', img)
                
                    printProgressBar(i*len(ims) + j, len(prj.classes)*len(ims), prefix = 'Extracting individual masks:', suffix = f'({i*len(ims) + j}/{len(prj.classes)*len(ims)})', length = 50)

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')