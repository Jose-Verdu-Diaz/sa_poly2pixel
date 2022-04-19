######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################
import os
import yaml
import argparse

from lib.auxiliary import bcolors, printHeader, printLoadedProject
from lib.createMask import createMask
from lib.createProjectJson import createProjectJson
from lib.loadExportedProject import loadExportedProject
from lib.loadProject import loadProject
from lib.loadPoly2PixProject import loadPoly2PixProject
from lib.projectExplorer import projectExplorer
from lib.analyseProject import analyseProject
#from lib.augmentateData import augmentateData
from lib.importImages import  importImages
from lib.importAnnotations import importAnnotations
from lib.configure import configure
from lib.imageReduction import imageReduction
from lib.editProject import editProject

def main(args):
    if not os.path.exists('config.yml'):
        default_config = dict(
            debug = False,
            projectDir = "./projects",
            exportedSaDir = "./projects"
        )

        with open('config.yml', 'w') as config_file:
            yaml.dump(default_config, config_file, default_flow_style=False)

    config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
    config['debug'] = args.debug
    with open("config.yml",'w') as configFile:
        yaml.dump(config, configFile)

    if not os.path.exists(f'{config["projectDir"]}'):
        input(f'\n{bcolors.FAIL}Projects Folder not found (expected at {config["projectDir"]}), press a key to continue...{bcolors.ENDC}')
        return

    project = None

    menuOptions = {
    0 : 'Analyse project',
    1 : 'Create Masks',
    2 : 'Augmentate data',
    3 : 'Reduce dimensions and classes',
    4 : 'Edit project'}

    while True:

        os.system("clear")
        printHeader()
        printLoadedProject(project)

        if config['debug']: print(f'\n{bcolors.WARNING+bcolors.BOLD}\tDEBUG MODE{bcolors.ENDC}')

        print(f'\nProject dir: {config["projectDir"]}')

        print(
"""
\nChoose service you want to use :

┏━━━━━━━━━━━━━━ IMPORT ━━━━━━━━━━━━━┓
┃  1: Import SA project             ┃
┃  2: Import exported SA projects   ┃
┃  3: Import poly2pix project       ┃
┃  4: Open project explorer         ┃
┣━━━━━━━━━━━━━ ANALYSE ━━━━━━━━━━━━━┫
┃  5: {0}               ┃
┣━━━━━━━━━━━━━━ TOOLS ━━━━━━━━━━━━━━┫
┃  6: {1}                  ┃
┃  7: {2}               ┃
┃  8: {3} ┃
┃  9: {4}                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                 
  10: Configure
   0: Exit"""
        .format(*('\u0336'.join(menuOptions[opt]) + '\u0336' if project is None else menuOptions[opt] for opt in menuOptions)))

        if config['debug']:
            print(
"""{warning}
┏━━━━━━━━━━━━━ DEBUG ━━━━━━━━━━━━━┓
┃ d1: Load placeholder project    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{end}"""
            .format(warning = bcolors.WARNING, end = bcolors.ENDC)
            )
        ### 
        ### d1 : Loads the first project (if any) in the config['projectDir'] directoy. Does nothing if empty.
        ###


        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            exit()

        elif choice == '1':
            project = None
            project = loadProject()  
            importImages(project)
            importAnnotations(project)
            createProjectJson(project)

        elif choice == '2':
            project = None
            project = loadExportedProject(config)
            importImages(project)
            importAnnotations(project)
            createProjectJson(project)    

        elif choice == '3':
            project = None
            project = loadPoly2PixProject(False, config)
            importImages(project)
            importAnnotations(project)
            createProjectJson(project) 

        elif choice == '4':
            project = None
            project = projectExplorer(config)

        elif choice == '5':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass

            else:
                analyseProject(project)

        elif choice == '6':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            else:
                createMask(project)

        elif choice == '7':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            else: 
                #augmentateData(project, config)
                input(f'\n{bcolors.FAIL}Option not available, press a key to continue...{bcolors.ENDC}')
        
        elif choice == '8':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            else: imageReduction(project)

        elif choice == '9':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            else:
                editProject(project, config)

        elif choice == '10':
            config = configure(project,config)

        elif choice == 'd1':
            project = None
            project = loadPoly2PixProject(True, config)

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug", help="Launch in debug mode", action="store_true")
    return parser.parse_args()



if __name__ == "__main__":
    args = parseArguments()
    main(args)