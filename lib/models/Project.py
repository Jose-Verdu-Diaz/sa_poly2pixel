from lib.models.Image import Image
from lib.models.Muscle import Muscle

# Stores project data
class Project:
    def __init__(self, images:Image = None, classes:Muscle = None, projectDir:str = None, name:str = None):
        self.images = images
        self.classes = classes
        self.projectDir = projectDir
        self.name = name