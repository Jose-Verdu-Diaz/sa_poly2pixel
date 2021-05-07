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
                    error_flag = False

                    for i,file in enumerate(sorted(os.listdir(f'projects/{prj.name}/individual/{cls}'))):
                        img = cv2.imread(f'projects/{prj.name}/individual/{cls}/{file}',cv2.IMREAD_GRAYSCALE)
                        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                        if len(contours) > 1:
                            print(f'{bcolors.FAIL}{cls} ## {file} ## {len(contours)} ## {bcolors.ENDC}')

                            if not error_flag: 
                                log.write(f'### {prj.classes[int(cls)-1].name} ({cls}) ###\n')
                                error_flag=True

                            im = cv2.imread(f'projects/{prj.name}/img/{file.split("_")[0]}.jpg')                           
                            im_copy = im.copy()

                            false_positive = False
                            alpha = 0.8
                            for cont in contours: 
                                if cv2.contourArea(cont) <= 1:
                                    false_positive=True
                                    im_copy = cv2.drawContours(im_copy, [cont], -1, (0, 0, 255), -1)
                                else:
                                    im_copy = cv2.drawContours(im_copy, [cont], -1, (51, 197, 255), -1)
                            filled = cv2.addWeighted(im, alpha, im_copy, 1-alpha, 0)
                            for cont in contours: 
                                if cv2.contourArea(cont) <= 1:
                                    result = cv2.drawContours(filled, [cont], -1, (0, 0, 255), 0)
                                else:
                                    result = cv2.drawContours(filled, [cont], -1, (51, 197, 255), 0)
                                    
                            log.write(f'\t{file}\t[FALSE POSITIVE?]') if false_positive else log.write(f'\t{file}')

                            cv2.imwrite(f'projects/{prj.name}/logs/repeated_img/{file}', result)

                            log.write('\n')
                        if i+1 == len(sorted(os.listdir(f'projects/{prj.name}/individual/{cls}'))) and error_flag: log.write('\n')

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
                    error_flag = False

                    files= sorted(os.listdir(f'projects/{prj.name}/individual/{cls}'))
                    for j,file in enumerate(files):

                        img = cv2.imread(f'projects/{prj.name}/individual/{cls}/{file}',cv2.IMREAD_GRAYSCALE)
                        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                        if j==0: cache = 0

                        if cache == 0 and len(contours) == 0:
                            cache = 0
                        elif cache == 0 and len(contours) > 0:
                            cache = 1
                            contour_cache = contours
                        elif cache == 1 and len(contours) > 0:
                            cache = 1
                            contour_cache = contours
                        elif cache == 1 and len(contours) == 0:
                            cache = 2
                        elif cache == 2 and len(contours) == 0:
                            cache = 2
                        elif cache == 2 and len(contours) > 0:
                            if not error_flag:
                                for k,cont in enumerate(contours):
                                    pass
                                log.write(f'### {prj.classes[int(cls)-1].name} ({cls}) ###\n')
                                error_flag=True

                            print(f'\r{bcolors.FAIL}{cls} ## {files[i-1]} ## {len(contours)}{bcolors.ENDC}{"".join([*(" " for k in range(68))])}')
                            ## 68 is the part of the length of the progress bar, this is for "cleaning" the line. This is a dirty, hard-typed solution that should be improved.
                            log.write(f'\t{files[j-1]}\n')
                            cache = 1

                        printProgressBar(i*len(files) + j + 1, len(dirs)*len(files), prefix = 'Analysing individual masks:', suffix = 'Complete', length = 50)

                    if j+1 == len(sorted(os.listdir(f'projects/{prj.name}/individual/{cls}'))) and error_flag: log.write('\n')

            input('\nContinue')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')