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

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show segmentation ┃
            ┃ 2 : Show class        ┃
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
            showSequence("/home/pepv/Practiques/Segm/Software/sa_poly2pixel/masks/RM1/img", None, 50)

        elif choice == '2': 
            classId = int(input('\nSelect a class Id: '))

            showSequence("/home/pepv/Practiques/Segm/Software/sa_poly2pixel/masks/RM1/img", classId, 50)