######################################################################
##            github.com/Jose-Verdu-Diaz/sa_poly2pixel              ##
######################################################################

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
import glob
import json

from poly2pixel_ui import *

# Stores image data found in images/images.sa
class Image:
    def __init__(self, srcPath, name, imagePath, thumbPath):
        self.srcPath = srcPath
        self.name = name
        self.imagePath = imagePath
        self.thumbPath = thumbPath
        self.polygons = []

    def setPoly(self, polygons):
        self.polygons = polygons

# Defines a 2D point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Stores polygons from annotations.json
class Polygon:
    def __init__(self, classId, points):
        self.classId = classId
        self.points = points

# Stores classes from classes.json
class Class:
    def __init__(self, color, id, name):
        self.color
        self.id
        self.name

# Stores project data
class Project:
    def __init__(self, images:Image, classes:Class = None):
        self.images = images
        self.classes = classes

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        # SA project dir
        self.projectDir = ""

        # Loaded project
        self.project = None

        # Images will be shown here
        self.label.setText("")

        # Search SA dir btn
        self.browseBtn.setText("Presióname")
        self.browseBtn.clicked.connect(self.openFileNameDialog)

        # Parse polygons from json btn
        self.loadPoly.clicked.connect(self.loadPolyJSON)

        self.show()

    # Open dialog for locating the SA project folder
    def openFileNameDialog(self):

        # Open File Dialog only for directories
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)		
        if dlg.exec_():

            # Selected dirs
            #####################################################
            ##            It should only select one,           ##
            #                     fix needed                   ##
            #####################################################
            filenames = dlg.selectedFiles()
            self.projectDir = filenames[0]

            # Load images.sa
            with open(self.projectDir + '/images/images.sa') as f:
                data = json.load(f)

                images = []

                for image in data:
                    images.append(Image(image["srcPath"],image["name"],image["imagePath"],image["thumbPath"]))

                self.project = Project(images = images)

            with open(self.projectDir + '/classes.json') as f:
                data = json.load(f)

                classes = []

                for c in data:
                    images.append(Class(c["color"],c["id"],c["name"]))
                    print(c)

            '''
            for filename in glob.glob(self.projectDir + '/images/*.jpg'):
                print(filename)
                self.img_routes.append(filename)
                im = QPixmap(filename)
                image_list.append(im)
                self.label.setPixmap(im)
            '''
    
    def loadPolyJSON(self):
        with open(self.projectDir + '/annotations.json') as f:
            data = json.load(f)
                
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()