import DTS
from DTS import *
import _DTS
from _DTS import *
import Asist_Func
from Asist_Func import *
import Diode
from Diode import *


def __init__(self):

    while 1:
        print('Choose the DTS for the tests from the list:')
        num = input('Press the number of the GEN1 DTS: \n 0 - DTS core0 \n 1 - DTS core1 \n'
                     ' 2 - DTS core2 \n 3 - DTS core3 \n 4 - DTS atom \n')
        dts_num = int(num)
        if -1 < dts_num < 5:  # check the name is correct
            break

    self.name = listGEN1DTS[dts_num]
    self.NumOfDiode = 6
    for i in range(6):
        self.diodesList.append(Diode(i))


## catblk vref vbe vcomp check ## test 1
# Description:
def CATBLK_VREF_VBE_VCOMP_CHECK(self):
    Asist_Func.dts_enable(self)
    _DTS.DTS_TAP_Default_Check(self)


def PWRON_DTS_RD_VBE_Check(self):
    num_of_diodes = 2
    Asist_Func.dts_disable(self)
    for diode in range(num_of_diodes):
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, diode)
        Asist_Func.program_viewanasigsel(self, 6)  # Select the analog dft mux to out the RD VBE
        Asist_Func.dts_enable(self)
        Asist_Func.measure_analog_func(self, 6)  # Measure VBE2
        Asist_Func.dts_disable(self)


def PWRON_BGCORE_VBE_VCCBGR_VBG(self):
    Asist_Func.dts_disable(self)
    Asist_Func.set_any_bg_trim_code(self, 50)  # set bgrtrimcode  = 6'b110010 (0x30) =32+16+2 =50 #### verify!!!
    Asist_Func.program_viewanasigsel(self, 1)  # Select the analog dft mux to out the BGCORE VBE
    Asist_Func.dts_enable(self)
    Asist_Func.measure_analog_func(self, 1)  # Measure BGCORE VBE1
    Asist_Func.dts_disable(self)
    Asist_Func.program_viewanasigsel(self, 2)  # Select the analog dft mux to out the BGCORE VCCBGR, BGREF(Vbg)
    Asist_Func.dts_enable(self)
    Asist_Func.measure_analog_func(self, 2)  # Measure VCCBGR


def PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self):
    Asist_Func.dts_disable(self)
    cattrip_code = [0, 127]
    for code in cattrip_code:
        for i in range(gen1_diode_num):
            Asist_Func.insert_cattrip_code(self, code, i)  # Set the cattrip trim code=6'b000000
        Asist_Func.program_viewanasigsel(self, 5)  # Select the analog dft mux to out the cattrip Vreftrip out
        Asist_Func.dts_enable(self)
        Asist_Func.measure_analog_func(self, 5)  # Measure comp_vref
        Asist_Func.dts_disable(self)
        Asist_Func.program_viewanasigsel(self, 3)  # Select the analog dft mux to out the cattrip comparator output
        Asist_Func.dts_enable(self)
        Asist_Func.measure_analog_func(self, 3)  # Measure cattrip comparator output
        Asist_Func.dts_disable(self)


def DTS_RD_VBE_Check(self):

