import os
from lib.auxiliary import *
from lib.analyseProject_functions.analyseProject_Classes import *
from lib.analyseProject_functions.analyseProject_Images import *
from lib.analyseProject_functions.analyseProject_CheckErrors import *

def analyseProject(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'''
                 {bcolors.BOLD}Name:{bcolors.ENDC} {prj.name}
            {bcolors.BOLD}Directory:{bcolors.ENDC} {prj.projectDir}
         {bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}
        {bcolors.BOLD}Nº of classes:{bcolors.ENDC} {len(prj.classes) + 1}
        ''')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Classes           ┃
            ┃ 2 : Images            ┃
            ┃ 3 : Check errors      ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            ap_classes(prj)

        elif choice == '2':
            ap_images(prj)

        elif choice == '3':
            ap_checkErrors(prj)     

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')