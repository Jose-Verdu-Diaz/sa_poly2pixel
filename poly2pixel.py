######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################
import os, yaml, argparse

from lib.aux import *
from lib.createMask import *
from lib.createProjectJson import *
from lib.loadExportedProject import *
from lib.loadProject import *
from lib.loadPoly2PixProject import *
from lib.analyseProject import *
from lib.showSequence import *
from lib.augmentateData import *
from lib.importImages import *
from lib.importAnnotations import *

def main(args):
    config = yaml.load(open("config.yml"))
    config['debug'] = args.debug
    with open("config.yml",'w') as configFile:
        yaml.dump(config, configFile)

    project = None

    menuOptions = {
    0 : 'Import images',
    1 : 'Import annotations',
    2 : 'Analyse project',
    3 : 'Create Masks',
    4 : 'Export poly2pix project',
    5 : 'Augmentate data'}

    while True:

        os.system("clear")
        printHeader()
        printLoadedProject(project)

        if config['debug']: print(f'\n{bcolors.WARNING+bcolors.BOLD}\tDEBUG MODE{bcolors.ENDC}')

        print(
"""
\nChoose service you want to use :

┏━━━━━━━━━━━━━ IMPORT ━━━━━━━━━━━━┓
┃ 1 : Import SA project           ┃
┃ 2 : Import exported SA projects ┃
┃ 3 : Import poly2pix project     ┃
┃ 4 : {0}               ┃
┃ 5 : {1}          ┃
┣━━━━━━━━━━━━ ANALYSE ━━━━━━━━━━━━┫
┃ 6 : {2}             ┃
┣━━━━━━━━━━━━━ MASK ━━━━━━━━━━━━━━┫
┃ 7 : {3}                ┃
┣━━━━━━━━━━━━━ EXPORT ━━━━━━━━━━━━┫
┃ 8 : {4}     ┃
┣━━━━━━━━━━━ AUGMENTATE━━━━━━━━━━━┫
┃ 9 : {5}             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
0 : Exit"""
        .format(*('\u0336'.join(menuOptions[opt]) + '\u0336' if project is None else menuOptions[opt] for opt in menuOptions)))

        if config['debug']:
            print(
"""{warning}

┏━━━━━━━━━━━━━ DEBUG ━━━━━━━━━━━━━┓
┃ d1 : Load placeholder project   ┃
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

        elif choice == '2':
            project = None
            project = loadExportedProject()      

        elif choice == '3':
            project = None
            project = loadPoly2PixProject(False)

        elif choice == '4':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass

            else:
                importImages(project)
                input(f'\n{bcolors.OKGREEN}Images imported, press a key to continue...{bcolors.ENDC}')

        elif choice == '5':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass

            else:
                importAnnotations(project)
                input(f'\n{bcolors.OKGREEN}Annotations imported, press a key to continue...{bcolors.ENDC}')

        elif choice == '6':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass

            else:
                analyseProject(project)

        elif choice == '7':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            try:
                createMask(project)
            except Exception as e:
                print(str(e))
                input(f'\n{bcolors.FAIL}Error creating masks, press a key to continue...{bcolors.ENDC}')

        elif choice == '8':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass

            else:
                createProjectJson(project)
                input(f'\n{bcolors.OKGREEN}Project exported, press a key to continue...{bcolors.ENDC}')

        elif choice == '9':
            if project == None:
                input(f'\n{bcolors.FAIL}There is no project loaded, press a key to continue...{bcolors.ENDC}')
                pass
            else: augmentateData(project)


        elif choice == 'd1':
            project = None
            project = loadPoly2PixProject(True)

        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug", help="Launch in debug mode", action="store_true")
    return parser.parse_args()



if __name__ == "__main__":
    args = parseArguments()
    main(args)