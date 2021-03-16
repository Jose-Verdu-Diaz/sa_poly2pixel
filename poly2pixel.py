######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################
import os, sys, json
from PIL import Image, ImageDraw

from lib.models.project import Project
from lib.models.class_ import Class_
from lib.models.polygon import Polygon
from lib.models.image_ import Image_

from lib.aux import *
from lib.createMask import *
from lib.createProjectJson import *
from lib.loadExportedProject import *
from lib.loadProject import *
from lib.loadPoly2PixProject import *

def main():

    project = None

    while True:

        os.system("clear")
        printHeader()
        printLoadedProject(project)

        print("\nChoose service you want to use : ")
        print("""
        ━━━━━━━━━━━━ IMPORT ━━━━━━━━━━━━
        1 : Import SA project 
        2 : Import exported SA projects
        3 : Import poly2pix project

        ━━━━━━━━━━━━━ MASK ━━━━━━━━━━━━━
        4 : Create Masks

        ━━━━━━━━━━━━ EXPORT ━━━━━━━━━━━━
        5 : Export poly2pix project

        
        0 : Exit""")

        choice = input("\nEnter your choice : ")

        # Load project
        if choice == '0':
            exit()

        elif choice == '1':
            project = None
            project = loadProject()     

        elif choice == '2':
            project = None
            project = loadExportedProject()      

        elif choice == '3':
            project = None
            project = loadPoly2PixProject()

        elif choice == '4':
            createMask(project)

        elif choice == '5':
            createProjectJson(project)

        else:

            input('Unexpected option, press a key to continue')

if __name__ == "__main__":
    main()