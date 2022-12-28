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
    diodesList = []


    # methods
    def __init__(self):
        _DTS.__init__(self)

    def method(self):
        _DTS.method(self)

    ## BG TRIM STEP 1 ##
    # Description:
    # The function will get BG TRIM on of the following strings:
    # dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
    def bg_trim_step1(self):
        _DTS.bg_trim_step1(self)

    ## BG TRIM STEP 2 ##
    # Description:
    # The function will get BG TRIM on of the following strings:
    # dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
    def bg_trim_step2(self):
        _DTS.bg_trim_step2(self)

    ## Tap Defualt Check ##
    # Description:
    def DTS_TAP_Default_Check(self):  # test 1
        _DTS.DTS_TAP_Default_Check(self)

    ## TAP Write Read Check ##
    # Description:
    def DTS_TAP_Write_Read_Check(self):  # test 2
        _DTS.DTS_TAP_Write_Read_Check(self)

    ## CRI Defualt Check ##
    # Description:
    def DTS_CRI_Default_Check(self):  # test 3
        _DTS.DTS_CRI_Default_Check(self)

    ## CRI Write Read Check ##
    # Description:
    def DTS_CRI_Write_Read_check(self):  # test 4
        _DTS.DTS_CRI_Write_Read_check(self)

    ## Pre Trim Rawcode Readout ##
    # Description:
    def pretrim_rawcode_readout(self, temp):  # test 5
        _DTS.DTS_pretrim_rawcode_readout_particular_temp(self, temp)

    ## Trim the diodea ##
    ## Description:
    def DTS_trim_rawcode(self):
        _DTS.DTS_trim_rawcode(self)

    ## Post Trim Temp Readout ##
    # Description:
    def posttrim_temp_readout(self, temperature):  # test 6
        _DTS.DTS_posttrim_temp_readout(self, temperature)

    ## cat autotrim check ##
    # Description:
    def DTS_cat_autotrim_check(self, temperature):  # test 7
        _DTS.DTS_cat_autotrim_check(self, temperature)

    ## Cat 2 Points Auto Trim Check ##
    # Description:
    def cat_2point_autotrim_check(self, temperature):  # test 8
        _DTS.DTS_cat_2point_autotrim_check(self, temperature)

    ## Trim the diodea ##
    ## Description:
    def DTS_cat_trim_rawcode(self, cattrip_temperature):
        _DTS.DTS_cat_trim_rawcode(self, cattrip_temperature)

    ## Post Calib Catblk Check ##
    # Description:
    def postcalib_catblk_trim_check(self, temperature, cattrip_temperature):  # test 9
        _DTS.DTS_postcalib_catblk_trim_check(self, temperature, cattrip_temperature)

    ## BG wait time check ##
    # Description:
    def BG_WAIT_TIME_CHECK(self):  # test 9
        _DTS.BG_WAIT_TIME_CHECK(self)



if __name__ == '__main__':
    pass
