import os
import json

from lib.auxiliary import bcolors, printHeader, printTable
from lib.models.Image import Image
from lib.models.Muscle import Muscle
from lib.models.Project import Project
from lib.models.Polygon import Polygon

def projectExplorer(config):
    prj = Project()

    projectDirectories = sorted([d for d in os.listdir(config['projectDir']) if os.path.isdir(os.path.join(config['projectDir'], d))])
    projectIds = [str(idx) for idx in range(1,len(projectDirectories)+1)]

    while True:
        os.system("clear")
        printHeader()

        printTable(['Id','Project'],[projectIds,projectDirectories])
        print('\n0 : Exit')

        try:
            choice = input("\nSelect a project by id: ")
            # Raise error if not convertable to integer
            isInt = int(choice)
        except:
            choice = ''

        # Load project
        if choice == '0':
            return

        elif int(choice) in range(1,len(projectDirectories)+1):
            project = f'{config["projectDir"]}/{projectDirectories[int(choice)-1]}/project.json'

            with open(project) as f: data = json.load(f)

            prj.projectDir = data['projectDir']
            prj.name = data['name']

            images = []

            for img in data['images']:
                polygons = []

                for poly in img['polygons']:
                    points = []

                    for point in poly['points']: points.append((point['x'],point['y']))
                    polygons.append(Polygon(poly['classId'], points))
                
                images.append(Image(img['srcPath'],img['name'],img['imagePath'], img['thumbPath'], polygons))
            
            prj.images = images
            classes = []

            for cls in data['classes']:
                classes.append(Muscle(cls['color'], cls['id'], cls['name']))

            prj.classes = classes
                    
            return prj

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')