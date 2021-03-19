import os
from lib.aux import *

from lib.showSequence import *

def ap_images(prj):
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
            showSequence(f'{prj.projectDir}/img/', 0, 50)