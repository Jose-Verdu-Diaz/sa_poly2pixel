# Stores polygons from annotations.json
class Polygon:
    def __init__(self, classId, points):
        self.classId = classId
        self.points = points