import os, sys, cv2
import numpy as np
from PIL import Image, ImageDraw

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

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Search class errors        ┃
            ┃ 2 : Search missing annotations ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            if not os.path.exists(f'projects/{prj.name}/logs/repeated_img'):
                os.makedirs(f'projects/{prj.name}/logs/repeated_img')

            with open(f'projects/{prj.name}/logs/repeated_class.txt', 'w') as log:
                for cls in sorted(os.listdir(f'projects/{prj.name}/individual')):

                    log.write(f'### {prj.classes[int(cls)-1].name} ({cls}) ###\n')

                    for file in sorted(os.listdir(f'projects/{prj.name}/individual/{cls}')):
                        img = cv2.imread(f'projects/{prj.name}/individual/{cls}/{file}',cv2.IMREAD_GRAYSCALE)
                        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                        if len(contours) > 1:
                            print(f'{bcolors.FAIL}{cls} ## {file} ## {len(contours)}{bcolors.ENDC}')
                            log.write(f'\t{file}\n')

                            im = cv2.imread(f'projects/{prj.name}/masks/{file.split("_")[0]}.bmp')
                            f= os.path.splitext(f'{file.split("_")[0]}.bmp')[0]

                            im_copy = im.copy()

                            for j,img in enumerate(im_copy):
                                black_pixels_mask = np.all(img != [int(cls), int(cls), int(cls)], axis=-1)
                                non_black_pixels_mask = ~black_pixels_mask

                                img[black_pixels_mask] = [0, 0, 0]
                                img[non_black_pixels_mask] = [199, 65, 72]

                                cv2.imwrite(f'projects/{prj.name}/logs/repeated_img/{file}', img)

                    log.write('\n')

            input('Continue')

        elif choice == '2':

            if not os.path.exists(f'projects/{prj.name}/logs/missing_img'):
                os.makedirs(f'projects/{prj.name}/logs/missing_img')

            with open(f'projects/{prj.name}/logs/missing_class.txt', 'w') as log:
                dirs = sorted(os.listdir(f'projects/{prj.name}/individual'))

                files_aux= sorted(os.listdir(f'projects/{prj.name}/individual/{dirs[0]}'))
                printProgressBar(0, len(dirs)*len(files_aux), prefix = 'Analysing individual masks:', suffix = 'Complete', length = 50)

                for i,cls in enumerate(dirs):                   
                    ## Cache:
                    ##      0 - Initial black
                    ##      1 - The image before had content
                    ##      2 - The image before didn't had content

                    log.write(f'### {prj.classes[int(cls)-1].name} ({cls}) ###\n')

                    files= sorted(os.listdir(f'projects/{prj.name}/individual/{cls}'))
                    for j,file in enumerate(files):

                        img = cv2.imread(f'projects/{prj.name}/individual/{cls}/{file}',cv2.IMREAD_GRAYSCALE)
                        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                        if j==0: cache = 0

                        if cache == 0 and len(contours) == 0:
                            cache = 0
                        elif cache == 0 and len(contours) > 0:
                            cache = 1
                        elif cache == 1 and len(contours) > 0:
                            cache = 1
                        elif cache == 1 and len(contours) == 0:
                            cache = 2
                        elif cache == 2 and len(contours) == 0:
                            cache = 2
                        elif cache == 2 and len(contours) > 0:
                            print(f'\r{bcolors.FAIL}{cls} ## {files[i-1]} ## {len(contours)}{bcolors.ENDC}{"".join([*(" " for k in range(68))])}')
                            ## 68 is the part of the length of the progress bar, this is for "cleaning" the line. This is a dirty, hard-typed solution that should be improved.
                            log.write(f'\t{files[j-1]}\n')
                            cache = 1

                        printProgressBar(i*len(files) + j, len(dirs)*len(files), prefix = 'Analysing individual masks:', suffix = 'Complete', length = 50)

                    log.write('\n')

            input('\nContinue')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')