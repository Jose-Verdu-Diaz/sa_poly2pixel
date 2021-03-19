import os
from lib.aux import *

def analyseProject(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print(f'''
                {bcolors.BOLD}Name:{bcolors.ENDC} {prj.name}
            {bcolors.BOLD}Directory:{bcolors.ENDC} {prj.projectDir}
        {bcolors.BOLD}Nº of images:{bcolors.ENDC} {len(prj.images)}
        {bcolors.BOLD}Nº of classes:{bcolors.ENDC} {len(prj.classes)}
        ''')

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Show classes      ┃
            ┃ 2 : Show images       ┃
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

        elif choice == '2':
            idList = []
            nameList = []
            nPolyList = []

            for i,img in enumerate(prj.images):
                idList.append(str(i))
                nameList.append(str(img.name))
                nPolyList.append(str(len(img.polygons)))
            printTable(['Id','Name','Nº of poly'],[idList,nameList,nPolyList])


        input('\nPress a key to continue...')