from .image_ import Image_
from .class_ import Class_

# Stores project data
class Project:
    def __init__(self, images:Image_ = None, classes:Class_ = None, projectDir:str = None, name:str = None):
        self.images = images
        self.classes = classes
        self.projectDir = projectDir
        self.name = name