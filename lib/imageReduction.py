import os
from lib.aux import *
from lib.analyseProject_functions.analyseProject_Classes import *
from lib.analyseProject_functions.analyseProject_Images import *
from lib.analyseProject_functions.analyseProject_CheckErrors import *
from lib.analyseProject_functions.analyseProject_EditProject import *

def imageReduction(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'''
        {bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)} > {len(prj.images)*2}
        {bcolors.BOLD}Nº of classes:{bcolors.ENDC} {len(prj.classes) + 1} > {int(len(prj.classes)/2) + 1}
        ''')

        print("""
            This tool selects only the right/left leg to
            reduce the dimension of the image and the
            amount of classes for image segmentation.

            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : TEST              ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        if choice == '0':
            return

        elif choice == '1':
            ap_classes(prj) 

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')