import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
import glob

from poly2pixel_ui import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    projectDir = ""

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self) 
        self.label.setText("Haz clic en el botón")
        self.browseBtn.setText("Presióname")
        self.browseBtn.clicked.connect(self.openFileNameDialog)

        self.show()

    def openFileNameDialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames[0])
            projectDir = filenames[0]

            image_list = []

            for filename in glob.glob(projectDir + '/*.jpg'):
                im = QPixmap(filename)
                image_list.append(im)
                self.label.setPixmap(im)
                
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()