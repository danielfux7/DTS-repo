## DTSGEN1 Class ##
import _DTSGEN1
from _DTSGEN1 import *


class DTSGEN1(DTS):
    # Variables
    name = "dts"
    temperature = 25 # default
    NumOfDiode = 6
    diodesList = []
    adc_linearity_check = []  # [voltage applied , raw code ]
    adc_slope = 0
    adc_offset = 0
    bgrtrimcode = 63
    gen = 1
    pre_trim_all_diodes_data = {}
    slope_offset_all_diodes_data = {}
    post_trim_all_diodes_data = {}
    cat_pre_trim_all_diodes_data = {}
    cat_trim_all_diodes_data = {}
    catblk_post_calib_data = {}
    VBE_check_data_gen1 = {}
    PWRON_BGCORE_VBE_VCCBGR_VBG_data = {}
    CATBLK_VREF_VBE_VCOMP_CHECK_data = {}
    DTS_CATTRIP_ALERT_CHK_EXTVBE_data = {}
    vccbgr_check_data = {}
    sd_adc_linearity_check_data = {}
    vbe_diode0 = -1


    # methods
    def __init__(self, name):
        _DTSGEN1.__init__(self, name)

    def BGR_calib_gen1(self, bgrtrimcode):
        _DTSGEN1.BGR_calib_gen1(self, bgrtrimcode)

    # test 1
    def DTS_GEN1_TAP_DEFAULT_CHECK(self):
        _DTSGEN1.DTS_GEN1_TAP_DEFAULT_CHECK(self)

    # test 2
    def PWRON_DTS_RD_VBE_Check(self, temperature):
        _DTSGEN1.PWRON_DTS_RD_VBE_Check(self, temperature)

    # test 3
    def PWRON_BGCORE_VBE_VCCBGR_VBG(self, bgtrimcode):
        _DTSGEN1.PWRON_BGCORE_VBE_VCCBGR_VBG(self, bgtrimcode)

    # test 4
    def PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self):
        _DTSGEN1.PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self)

    # test 8
    def DTS_VCCBGR_CHECK(self):
        _DTSGEN1.DTS_VCCBGR_CHECK(self)

    # tests 9 and 11
    def DTS_PRETRIM_RAWCODE_READOUT(self, temperature, buf_en):
        _DTSGEN1.DTS_PRETRIM_RAWCODE_READOUT(self, temperature, buf_en)

    # Trim the diodes
    def DTS_trim_gen1(self, buf_en):
        _DTSGEN1.DTS_trim_gen1(self, buf_en)

    # tests 10 and 12
    def DTS_POSTTRIM_TEMP_READOUT(self, temperature, buf_en):
        _DTSGEN1.DTS_POSTTRIM_TEMP_READOUT(self, temperature, buf_en)

    ## DTS full accuracy function  ##
    def DTS_full_accuracy_func_gen1(self, buf_en):
        _DTSGEN1.DTS_full_accuracy_func_gen1(self,buf_en)

    # test 13
    def DTS_ADC_Linearity_check(self):
        _DTSGEN1.DTS_ADC_Linearity_check(self)

    # test 14
    def DTS_CAT_AUTOTRIM_CHECK(self, temperature):
        _DTSGEN1.DTS_CAT_AUTOTRIM_CHECK(self,temperature)

    # test 14.5
    def DTS_CAT_TRIM_GEN1(self, cattrip_temperature):
        _DTSGEN1.DTS_CAT_TRIM_GEN1(self, cattrip_temperature)

    # test 15
    def DTS_POSTCALIB_CATBLK_TRIP_CHECK(self, temperature_start_point,target_temperature):
        _DTSGEN1.DTS_POSTCALIB_CATBLK_TRIP_CHECK(self, temperature_start_point, target_temperature)

    ## DTS full cattrip calib function gen1 ##
    def DTS_full_cattrip_calib_func_gen1(self):
        _DTSGEN1.DTS_full_cattrip_calib_func_gen1(self)

    # test 16
    def CATBLK_VREF_VBE_VCOMP_CHECK(self):
        _DTSGEN1.CATBLK_VREF_VBE_VCOMP_CHECK(self)

    # test 20
    def DTS_CATTRIP_ALERT_CHK_EXTVBE(self):
        _DTSGEN1.DTS_CATTRIP_ALERT_CHK_EXTVBE(self)

    # test 21
    def DTS_AVG_SUPLKG_CHECK_ONESHOTMODE(self):
        _DTSGEN1.DTS_AVG_SUPLKG_CHECK_ONESHOTMODE(self)

