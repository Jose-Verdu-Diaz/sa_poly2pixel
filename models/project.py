from .image import Image
from .class_ import Class_

# Stores project data
class Project:
    def __init__(self, images:Image = None, classes:Class_ = None, projectDir:str = None):
        self.images = images
        self.classes = classes
        self.projectDir = projectDir