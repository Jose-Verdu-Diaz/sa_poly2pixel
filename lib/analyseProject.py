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

            1 : Print classes 
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif choice == '1':
            for cls in prj.classes:
                # Get hex color and strip '#'
                colorHex = cls.color.lstrip('#')
                # Convert hex color to rgb
                colorRGB = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))

                print(f'{get_color_escape(colorRGB[0],colorRGB[1],colorRGB[2], True)}{cls.id}{bcolors.ENDC} : {get_color_escape(colorRGB[0],colorRGB[1],colorRGB[2])}{cls.name}{bcolors.ENDC}')
        
        input('\nPress a key to continue...')