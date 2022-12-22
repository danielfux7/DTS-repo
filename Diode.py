# Class Diode

class Diode:
    pretrimData = []  # [Temperature, mean, max , min]
    diodeNum = -1
    valid = True
    slope = -1
    offset = -1

    posttrimData = {
        '256_avgen': -1,
        '512_avgen': -1,
        '1024_avgen': -1,
        '2048_avgen': -1,
        '256_disgen': -1,
        '512_disen': -1,
        '1024_disgen': -1,
        '2048_disgen': -1,
    }



    def __init__(self, diodeNum):
        self.diodeNum = diodeNum

