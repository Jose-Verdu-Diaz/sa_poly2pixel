import os
from lib.auxiliary import *
from lib.showSequence import *

def ap_classes(prj):

    save = False

    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        idList = []
        nameList = []
        colorList = []

        # Stores tick and cross symbols for the menu 
        tick = dict([(True, f'{bcolors.OKGREEN}{bcolors.BOLD}✔{bcolors.ENDC}'), (False, f'{bcolors.FAIL}{bcolors.BOLD}✘{bcolors.ENDC}')])

        for cls in prj.classes:
            idList.append(str(cls.id))
            nameList.append(str(cls.name))
            colorHex = cls.color.lstrip('#')
            colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))
            colorList.append(get_color_escape(colorRGB[0],colorRGB[1],colorRGB[2], True))

        printTable(['Id','Name','Color'],[idList,nameList,''],colorList)

        print(f'\nSave animation: {"".join(tick[save])}')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show segmentation (B&W)   ┃
            ┃ 2 : Show segmentation (Color) ┃
            ┃ 3 : Show class                ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

            4 : Save animation
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            showSequence(prj,'masks', None, 50, save)
        
        elif choice == '2':
            showSequence(prj,'masks_color', None, 50, save)

        elif choice == '3': 
            classId = int(input('\nSelect a class Id: '))

            showSequence(prj,'masks', classId, 50, save)

        elif choice == '4':
            save = not save

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')