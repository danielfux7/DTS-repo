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
    def pretrim_rawcode_readout(self, temp, bgWait):  # test 5
        _DTS.DTS_pretrim_rawcode_readout_particular_temp(self, temp, bgWait)

    ## Trim the diodea ##
    ## Description:
    def DTS_trim_rawcode(self, bgWait):
        _DTS.DTS_trim_rawcode(self, bgWait)

    ## Post Trim Temp Readout ##
    # Description:
    def posttrim_temp_readout(self, temperature, bgWait):  # test 6
        _DTS.DTS_posttrim_temp_readout(self, temperature, bgWait)

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
    def DTS_cat_trim_rawcode(self, cattrip_temperature):  # test 8.5
        _DTS.DTS_cat_trim_rawcode(self, cattrip_temperature)

    ## Post Calib Catblk Check ##
    # Description:
    def postcalib_catblk_trim_check(self, temperature, cattrip_temperature):  # test 9
        _DTS.DTS_postcalib_catblk_trim_check(self, temperature, cattrip_temperature)

    ## BG wait time check ##
    # Description:
    def BG_WAIT_TIME_CHECK(self, waitDelay):  # test 11
        _DTS.BG_WAIT_TIME_CHECK(self, waitDelay)

    ## BG wait code check ##
    # Description:
    def BG_WAIT_CODE_CHECK(self, temperature, bgWait):  # test 12
        _DTS.BG_WAIT_CODE_CHECK(self, bgWait)

    ## sleep delay check ##
    # Description:
    def SLEEP_DELAY_CHECK(self, sleepTime):  # test 12
        _DTS.SLEEP_DELAY_CHECK(self, sleepTime)

    ## dynamic skeep delay check ##
    # Description:
    def DYNAMIC_SLEEP_DELAY_CHECK(self, sleepTime):  # test 13
        _DTS.DYNAMIC_SLEEP_DELAY_CHECK(self, sleepTime)

    ## adc clock div test ##
    # Description:
    def ADC_CLK_DIV_TEST(self, temperature):  # test 14
        _DTS.ADC_CLK_DIV_TEST(self, temperature)

    ## DTD ns alert test ## test 16
    def DTD_NS_ALERT_TEST(self, temperature, threshold, direction ):
        _DTS.DTD_NS_ALERT_TEST(self, temperature, threshold, direction)

    ## DTD sticky alert test ## test 17
    def DTD_STICKY_ALERT_TEST(self, maxTemperature, minTemperature, lowLimit, highLimit):
        _DTS.DTD_STICKY_ALERT_TEST(self, maxTemperature, minTemperature, lowLimit, highLimit)

    ## bgcore bgg vtrim ## test 19
    def BGCORE_VBG_vtrim(self, bgtrimcode, tc):
        _DTS.BGCORE_VBG_vtrim(self, bgtrimcode, tc)

    ## DTS pre trim bg ref check ## test 20
    def DTS_PRETRIM_BGREF_CHECK(self):
        _DTS.DTS_PRETRIM_BGREF_CHECK(self)



    ## ana pwr seq view ##
    def ANA_PWR_SEQ_VIEW(self, viewpin1Signal):  # test 24
        _DTS.ANA_PWR_SEQ_VIEW(self, viewpin1Signal)

if __name__ == '__main__':
    pass
