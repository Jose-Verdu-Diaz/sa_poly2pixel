import os
from lib.auxiliary import *

from lib.showSequence import *

def ap_images(prj):

    save = False

    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        idList = []
        nameList = []
        nPolyList = []

        # Stores tick and cross symbols for the menu 
        tick = dict([(True, f'{bcolors.OKGREEN}{bcolors.BOLD}✔{bcolors.ENDC}'), (False, f'{bcolors.FAIL}{bcolors.BOLD}✘{bcolors.ENDC}')])

        for i,img in enumerate(prj.images):
            idList.append(str(i))
            nameList.append(str(img.name))
            nPolyList.append(str(len(img.polygons)))
        printTable(['Id','Name','Nº of poly'],[idList,nameList,nPolyList])

        print(f'\nSave animation: {"".join(tick[save])}')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show images       ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━┛
            
            2 : Save animation

            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            showSequence(prj,'img', None, 50, save)

        elif choice == '2':
            save = not save

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')