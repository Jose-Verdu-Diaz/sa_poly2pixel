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
            if not os.path.exists(f'masks/{prj.name}/logs'):
                os.makedirs(f'masks/{prj.name}/logs')

            with open(f'masks/{prj.name}/logs/repeated_class.txt', 'w') as log:
                for cls in sorted(os.listdir(f'masks/{prj.name}/individual')):

                    log.write(f'### {prj.classes[int(cls)-1].name} ({cls}) ###\n')

                    for file in sorted(os.listdir(f'masks/{prj.name}/individual/{cls}')):
                        img = cv2.imread(f'masks/{prj.name}/individual/{cls}/{file}',cv2.IMREAD_GRAYSCALE)
                        contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                        if len(contours) > 1:
                            print(f'{bcolors.FAIL}{cls} ## {file} ## {len(contours)}{bcolors.ENDC}')
                            log.write(f'\t{file}\n')

                    log.write('\n')

            input('Continue')

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')