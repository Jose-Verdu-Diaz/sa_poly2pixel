import os, yaml, shutil
import tkinter as tk
from tkinter import filedialog
from lib.aux import *

def configure(prj,config):
    while True:
        os.system("clear")
        printHeader()
        printLoadedProject(prj)

        print("""
            \nChoose an option:

            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ 1 : Change projects folder             ┃
            ┃ 2 : Change exported SA projects folder ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            
            0 : Exit""")

        try:
            choice = input("\nEnter your choice : ")
        except:
            choice = ''

        # Load project
        if choice == '0':
            return config

        elif choice == '1':
            # Directory explorer
            root = tk.Tk()
            root.withdraw()

            new_location = filedialog.askdirectory()

            if not new_location + '/projects' == config['projectDir']:
                if os.path.exists(config["projectDir"]):
                    shutil.move(config["projectDir"], new_location)

                config['projectDir'] = new_location + '/projects'

                with open("config.yml",'w') as configFile:
                    yaml.dump(config, configFile)

        elif choice == '2':
            # Directory explorer
            root = tk.Tk()
            root.withdraw()
            
            config['exportedSaDir'] = filedialog.askdirectory()

            with open("config.yml",'w') as configFile:
                yaml.dump(config, configFile)


        else:
            input(f'\n{bcolors.FAIL}Unexpected option, press a key to continue...{bcolors.ENDC}')