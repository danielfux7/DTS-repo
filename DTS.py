## DTS Class ##
import namednodes as _namednodes
from config import *
import _DTS
from _DTS import *

class DTS:
    # Variables
    name = "dts"
    temperature = 25 # default
    Step1TrimValue = -1
    Step2TrimValue = -1
    NumOfDiode = -1

    # methods
    def __init__(self):
        _DTS.__init__(self)

    def method(self):
        _DTS.method(self)

    def bg_trim_step1(self):
        _DTS.bg_trim_step1(self)

    def bg_trim_step2(self):
        _DTS.bg_trim_step2(self)

    def pretrim_rawcode_readout(self):  # test 5
        _DTS.pretrim_rawcode_readout(self)

    def posttrim_temp_readout(self):  # test 6
        _DTS.posttrim_temp_readout(self)

    def cat_2point_autotrim_check(self):  # test 8
        _DTS.cat_2point_autotrim_check(self)

    def postcalib_catblk_trip_check(self):  # test 9
        _DTS.postcalib_catblk_trip_check(self)


if __name__ == '__main__':
    pass
