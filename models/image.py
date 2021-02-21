class Image:
    def __init__(self, srcPath, name, imagePath, thumbPath):
        self.srcPath = srcPath
        self.name = name
        self.imagePath = imagePath
        self.thumbPath = thumbPath
        self.polygons = []

    def setPoly(self, polygons):
        self.polygons = polygons