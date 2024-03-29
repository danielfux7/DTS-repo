## DTS Class ##
import namednodes as _namednodes
from config import *
import _DTS
from _DTS import *
import Diode
from Diode import *


class DTS:
    # Variables
    name = "dtsgen2"
    temperature = 25 # default
    Step1TrimValue = -1
    Step2TrimValue = -1
    NumOfDiode = -1
    diodesList = []
    adc_linearity_check = []  # [voltage applied , raw code ]
    adc_dynamic_check = []  # [freq, elapsed_time, curr_voltage_applied, raw code]
    adc_slope = 0
    adc_offset = 0
    gen = 2
    bgrtrimcode_data = {}
    pre_trim_all_diodes_data = {}
    slope_offset_all_diodes_data = {}
    post_trim_all_diodes_data = {}
    cat_pre_trim_all_diodes_data = {}
    cat_trim_all_diodes_data = {}
    catblk_post_calib_data = {}
    catblk_vref_vbe_vcomp_data = {}
    VBE_check_data = {}
    sleep_delay_check_data = {}
    pre_trim_bg_ref_data = {}
    post_trim_bg_ref_data = {}
    bg_ref_default_check_data = {}
    bg_wait_code_data = {}
    bg_wait_time_data = {}
    ADCclkDivData = {}
    adc_clk_all_data = {}
    sd_adc_linearity_check_data = {}
    sd_adc_dynamic_check_data = {}
    DTD_NS_alert_direction_0_data = {}
    DTD_NS_alert_direction_1_data = {}
    DTD_sticky_alert_data = {}
    ana_pwr_seq_data = {}
    CATBLK_VREF_VBE_VCOMP_data = {}
    fusa_check = {}
    path = r'C:\Users\daniel\results'

    # save data for gen1 excel
    slope_offset_all_diodes_gen1_data = {}
    cat_trim_all_diodes_gen1_data = {}

    # methods
    def __init__(self, name):
        _DTS.__init__(self, name)

    def method(self):
        _DTS.method(self)

    ## BG TRIM STEP 1 ##
    # Description:
    # The function will get BG TRIM on of the following strings:
    # dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
    def bg_trim_step1(self):
        _DTS.DTS_bg_trim_step1(self)

    ## BG TRIM STEP 2 ##
    # Description:
    # The function will get BG TRIM on of the following strings:
    # dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
    def bg_trim_step2(self):
        _DTS.DTS_bg_trim_step2(self)

    ## Tap Defualt Check ##
    # Description:
    def DTS_TAP_Default_Check(self):  # test 1
        _DTS.DTS_TAP_Default_Check(self)

    ## Write Values to Tap Registers ##
    # Description: this function will insert values to Tap registers(dtsfusecfg,tapconfig,tapstatus)
    def DTS_write_values_func(self):
        _DTS.DTS_write_values_func(self)

    ## TAP Write Read Check ##
    # Description:
    def DTS_TAP_Write_Read_Check(self):  # test 2
        _DTS.DTS_TAP_Write_Read_Check(self)

    ## CRI Defualt Check ##
    # Description:
    def DTS_CRI_Default_Check(self):  # test 3
        _DTS.DTS_CRI_Default_Check(self)

    ## Write Values to CRI Registers ##
    # Description: this function will insert values to CRI registers
    def DTS_write_values_to_CRI(self):
        _DTS.DTS_write_values_to_CRI(self)

    ## CRI Write Read Check ##
    # Description:
    def DTS_CRI_Write_Read_check(self):  # test 4
        _DTS.DTS_CRI_Write_Read_check(self)

    ## Taps VS CRI ##
    # Description:
    def taps_against_cri(self):
        _DTS.taps_against_cri(self)

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

    ## DTS full accuracy function  ##
    def DTS_full_accuracy_func(self):
        _DTS.DTS_full_accuracy_func(self)

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
    def postcalib_catblk_trim_check(self, temperature_start_point, cattrip_temperature):  # test 9
        _DTS.DTS_postcalib_catblk_trim_check(self, temperature_start_point, cattrip_temperature)

    ## DTS full cattrip calib function  ##
    def DTS_full_cattrip_calib_func(self):
        _DTS.DTS_full_cattrip_calib_func(self)

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
    def SLEEP_DELAY_CHECK(self, sleepTime, sleepTimeDynamic):  # test 12
        _DTS.SLEEP_DELAY_CHECK(self, sleepTime, sleepTimeDynamic)

    ## dynamic skeep delay check ##
    # Description:
    def DYNAMIC_SLEEP_DELAY_CHECK(self, sleepTime):  # test 13
        _DTS.DYNAMIC_SLEEP_DELAY_CHECK(self, sleepTime)

    ## adc clock div test ##
    # Description:
    def ADC_CLK_DIV_TEST(self, temperature, diode):  # test 14
        _DTS.ADC_CLK_DIV_TEST(self, temperature, diode)

    ## AON_OVRD_DTS_FUNC_CHECK ##
    def AON_OVRD_DTS_FUNC_CHECK(self):  # test 15
        _DTS.AON_OVRD_DTS_FUNC_CHECK(self)

    ## DTD ns alert test ## test 16
    def DTD_NS_ALERT_TEST(self, maxTemperature, minTemperature, threshold, direction):
        _DTS.DTD_NS_ALERT_TEST(self, maxTemperature, minTemperature, threshold, direction)

    ## DTD sticky alert test ## test 17
    def DTD_STICKY_ALERT_TEST(self, maxTemperature, minTemperature, lowLimit, highLimit):
        _DTS.DTD_STICKY_ALERT_TEST(self, maxTemperature, minTemperature, lowLimit, highLimit)

    ## bgcore bgg vtrim ## test 19
    def BGCORE_VBG_vtrim(self, bgtrimcode, tc):
        _DTS.BGCORE_VBG_vtrim(self, bgtrimcode, tc)

    ## DTS pre trim bg ref check ## test 19
    def DTS_DEFAULT_BGREF_CHECK(self):
        _DTS.DTS_DEFAULT_BGREF_CHECK(self)

    ## DTS pre trim bg ref check ## test 20
    def DTS_PRETRIM_BGREF_CHECK(self):
        _DTS.DTS_PRETRIM_BGREF_CHECK(self)

    ## DTS post trim bgref check ##
    def DTS_POSTTRIM_BGREF_CHECK(self):
        _DTS.DTS_POSTTRIM_BGREF_CHECK(self)

    ## Dithering ## test 25
    def dithering(self):
        _DTS.dithering(self)

    ## VBE check ##
    def DTS_RD_VBE_Check(self, temperature):
        _DTS.DTS_RD_VBE_Check(self, temperature)

    ## ana pwr seq view ##
    def ANA_PWR_SEQ_VIEW(self):  # test 24
        _DTS.ANA_PWR_SEQ_VIEW(self)

    ## CATBLK_VREF_VBE_VCOMP_CHECK ##
    def CATBLK_VREF_VBE_VCOMP_CHECK(self):
        _DTS.CATBLK_VREF_VBE_VCOMP_CHECK(self)

    ## ADC Linearity check ##
    def DTS_SD_ADC_Linearity_check(self, voltage_step_size):
        _DTS.DTS_SD_ADC_Linearity_check(self, voltage_step_size)

    ## ADC dynamic check ##
    def DTS_SD_ADC_dynamic_check(self):
        _DTS.DTS_SD_ADC_dynamic_check(self)

    ## fusa_check ##
    def bgr_fusa_check(self):
        _DTS.bgr_fusa_check(self)


if __name__ == '__main__':
    pass
