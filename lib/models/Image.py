class Image:
    def __init__(self, srcPath, name, imagePath, thumbPath, polygons = []):
        self.srcPath = srcPath
        self.name = name
        self.imagePath = imagePath
        self.thumbPath = thumbPath
        self.polygons = polygons

    def setPoly(self, polygons):
        self.polygons = polygons