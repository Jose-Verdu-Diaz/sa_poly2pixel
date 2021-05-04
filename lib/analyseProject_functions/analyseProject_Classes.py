import os
from lib.aux import *
from lib.showSequence import *

def ap_classes(prj):

    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        idList = []
        nameList = []
        colorList = []

        for cls in prj.classes:
            idList.append(str(cls.id))
            nameList.append(str(cls.name))
            colorHex = cls.color.lstrip('#')
            colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))
            colorList.append(get_color_escape(colorRGB[0],colorRGB[1],colorRGB[2], True))

        printTable(['Id','Name','Color'],[idList,nameList,''],colorList)

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show segmentation (B&W)   ┃
            ┃ 2 : Show segmentation (Color) ┃
            ┃ 3 : Show class                ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            showSequence(f'{os.getcwd()}/projects/{prj.name}/masks', None, 50)
        
        elif choice == '2':
            showSequence(f'{os.getcwd()}/projects/{prj.name}/masks_color', None, 50)

        elif choice == '3': 
            classId = int(input('\nSelect a class Id: '))

            showSequence(f'{os.getcwd()}/projects/{prj.name}/masks', classId, 50)

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')