# Class BgwaitPostTrim

class BgwaitPostTrim:

    Data = {}
    bgWait = -1

    def __init__(self, bgWait):
        self.bgWait = bgWait
        self.Data = {
            '256_avgdis': [],
            '512_avgdis': [],
            '1024_avgdis': [],
            '2048_avgdis': [],
            '256_avgen': [],
            '512_avgen': [],
            '1024_avgen': [],
            '2048_avgen': [],
        }
