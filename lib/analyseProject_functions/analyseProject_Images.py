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

        for i,img in enumerate(prj.images):
            idList.append(str(i))
            nameList.append(str(img.name))
            nPolyList.append(str(len(img.polygons)))
        printTable(['Id','Name','Nº of poly'],[idList,nameList,nPolyList])

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show images       ┃
            ┃                       ┃
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
            showSequence(prj,'img', None, 50, save)

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')