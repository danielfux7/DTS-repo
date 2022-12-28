# Class Diode

class Diode:
    pretrimData = []  # [Temperature, mean, max , min]
    diodeNum = -1
    valid = True
    slope = -1
    offset = -1
    catSlope = -1
    catOffset = -1
    posttrimData = {}
    catAutoTrimData = []
    cat2PointsTrimData = []
    postCalibData = {}

    def __init__(self, diodeNum):
        self.diodeNum = diodeNum
        self.posttrimData = {
            '256_avgdis': [],
            '512_avgdis': [],
            '1024_avgdis': [],
            '2048_avgdis': [],
            '256_avgen': [],
            '512_avgen': [],
            '1024_avgen': [],
            '2048_avgen': [],
        }
        self.pretrimData = []
        self.catAutoTrimData = []
        self.cat2PointsTrimData = []
        self.postCalibData = {}



