import os, json

from lib.aux import *
from lib.showSequence import *
from lib.aux import *


def ap_editProject(prj):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Shift class id (imported)    ┃
            ┃ 2 : Shift class id (unimported)  ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        ## Shifts the class Id of the polygons of the poly2pixel project
        elif choice == '1':
            shift = int(input('Shift classes id by:'))

            if prj.classes[0].id + shift < 1:              
                input(f'The resulting first class will have an index of {str(prj.classes[0].id + shift)}. That is not possible.\nContinue...')
            else:
                length = 0
                for img in prj.images: 
                    for ply in img.polygons:length += 1
                for cls in prj.classes:length += 1

                printProgressBar(0, length, prefix = 'Shifting id:', suffix = 'Complete', length = 50)
                i = 0
                for cls in prj.classes:
                    cls.id = cls.id + shift
                    i += 1
                    printProgressBar(i, length, prefix = 'Shifting id:', suffix = 'Complete', length = 50)
                for img in prj.images:
                    for ply in img.polygons:
                        ply.classId = ply.classId + shift
                        i += 1
                        printProgressBar(i, length, prefix = 'Shifting id:', suffix = 'Complete', length = 50)

                input(f'Continue...')

        ## Shifts the class Id of the annotations files of the exported SA project
        elif choice == '2':      

            shift = int(input('Shift classes id by:'))

            if prj.classes[0].id + shift < 1:              
                input(f'The resulting first class will have an index of {str(prj.classes[0].id + shift)}. That is not possible.\nContinue...')
            else:
                annotation_files = sorted(os.listdir(f'{prj.projectDir}/annotations'))

                printProgressBar(0, len(annotation_files), prefix = 'Shifting id:', suffix = 'Complete', length = 50)

                # For each annotation file, apply shift to id and save
                for i,file in enumerate(annotation_files):
                    with open(f'{prj.projectDir}/annotations/{file}') as f: data = json.load(f)                       
                    for d in data['instances']: d["classId"] += shift
                    with open(f'{prj.projectDir}/annotations/{file}', "w+") as f: f.write(json.dumps(data))

                    printProgressBar(i+1, len(annotation_files), prefix = 'Shifting id:', suffix = 'Complete', length = 50)
            
                input(f'\nContinue...')            

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')