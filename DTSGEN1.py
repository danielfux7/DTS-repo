## DTSGEN1 Class ##
import _DTSGEN1
from _DTSGEN1 import *

class DTSGEN1(DTS):
    # Variables
    name = "dts"
    temperature = 25 # default
    Step1TrimValue = -1
    Step2TrimValue = -1
    NumOfDiode = 6
    diodesList = []

    # methods
    def __init__(self):
        _DTSGEN1.__init__(self)

    # test 1
    def CATBLK_VREF_VBE_VCOMP_CHECK(self):
        _DTSGEN1.CATBLK_VREF_VBE_VCOMP_CHECK(self)

    # test 2
    def PWRON_DTS_RD_VBE_Check(self):
        _DTSGEN1.PWRON_DTS_RD_VBE_Check(self)

    # test 3
    def PWRON_BGCORE_VBE_VCCBGR_VBG(self):
        _DTSGEN1.PWRON_BGCORE_VBE_VCCBGR_VBG(self)

    # test 4
    def PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self):
        _DTSGEN1.PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self)
