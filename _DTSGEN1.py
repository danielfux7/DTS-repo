import DTS
from DTS import *
import _DTS
from _DTS import *
import Asist_Func
from Asist_Func import *
import Diode
from Diode import *


def __init__(self, name):

    # while 1:
    #     print('Choose the DTS for the tests from the list:')
    #     num = input('Press the number of the GEN1 DTS: \n 0 - DTS core0 \n 1 - DTS core1 \n'
    #                  ' 2 - DTS core2 \n 3 - DTS core3 \n 4 - DTS atom \n')
    #     dts_num = int(num)
    #     if -1 < dts_num < 5:  # check the name is correct
    #         break

    # self.name = listGEN1DTS[dts_num]
    self.name = name
    self.NumOfDiode = 6,
    self.VBE_check_data_gen1 = {}
    for i in range(6):
        self.diodesList.append(Diode(i))


## catblk vref vbe vcomp check ## test 1
# Description:
def DTS_GEN1_TAP_DEFAULT_CHECK(self):
    Asist_Func.dts_enable(self)
    _DTS.DTS_TAP_Default_Check(self)


def PWRON_DTS_RD_VBE_Check(self):
    _DTS.DTS_RD_VBE_Check(self)
    # num_of_diodes = 2
    # Asist_Func.dts_disable(self)
    # Asist_Func.program_viewanasigsel(self, 6)  # Select the analog dft mux to out the RD VBE
    #
    #
    # for diode in range(num_of_diodes):
    #     Asist_Func.diode_sel_ovr_en(self)
    #     Asist_Func.diode_sel_ovr_val(self, diode)
    #     Asist_Func.dts_enable(self)
    #     Asist_Func.measure_analog_func(self, 6)  # Measure VBE2
    #     Asist_Func.dts_disable(self)


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


def DTS_VCCBGR_CHECK(self):
    # measures = [bgadj , tc]
    measures = [[0, 4], [0, 3], [0, 0], [1, 4], [1, 3], [1, 0], [2, 4], [2, 3], [2, 0], [3, 4], [3, 3], [3, 0]],
    Asist_Func.dts_disable(self)
    Asist_Func.program_viewanasigsel(self, 0)  # Select the analog dft mux to out the VCC_BGR from bgcore
    Asist_Func.dts_enable(self)
    for i in range(len(measures)):
        Asist_Func.set_any_bgradj(self, measures[i][0])
        Asist_Func.set_any_tc(self, measures[i][1])
        result = Asist_Func.measure_analog_func(self, 0) ### TBD in the measure analog func need to return the measure
        measures[i].append(result)
    bgradj = [item[0] for item in measures]
    bgrtc = [item[1] for item in measures]
    result = [item[2] for item in measures]
    final = {'bgradj': bgradj, 'bgrtc': bgrtc, 'result': result}
    print(final)


def DTS_PRETRIM_RAWCODE_READOUT(self, temperature, buf_en):
    Asist_Func.dts_disable(self)
    if buf_en:
        Asist_Func.adcvinbufsel_en(self)
    else:
        Asist_Func.adcvinbufsel_dis(self)
    Asist_Func.rawcode_en(self)
    Asist_Func.update_chosen_mask(self, 63)  # 6'h3F
    Asist_Func.dts_enable(self)
    data = []  # data = [temperature, raw code]
    for diode in range(gen1_diode_num):
        #if Asist_Func.valid_diode_check(self, diode):
        if True:  ###### for debug!!!!
            rawcode = Asist_Func.read_temperature_code(self, diode)
            data = [temperature, rawcode]
            if buf_en:
                self.diodesList[diode].pretrim_gen1_buf_en.append(data)
                print(self.diodesList[diode].pretrim_gen1_buf_en)
            else:
                self.diodesList[diode].pretrim_gen1_buf_dis.append(data)
                print(self.diodesList[diode].pretrim_gen1_buf_dis)
        else:
            print(str(diode) + ' is invalid')


def DTS_trim_gen1(self, buf_en):
    for diode in range(gen1_diode_num):
        if Asist_Func.valid_diode_check(self,diode):
            if buf_en:  #
                temperatures = [item[0] for item in self.diodesList[diode].pretrim_gen1_buf_en]
                rawcodes = [item[1] for item in self.diodesList[diode].pretrim_gen1_buf_en]
            else:
                temperatures = [item[0] for item in self.diodesList[diode].pretrim_gen1_buf_dis]
                rawcodes = [item[1] for item in self.diodesList[diode].pretrim_gen1_buf_dis]

            slope, offset = Asist_Func.calculate_slope_and_offset(rawcodes, temperatures)
            print('slope: ' + str(slope))
            print('offset: ' + str(offset))
            Asist_Func.insert_slope_offset_to_diode(self, diode, slope, offset)


def DTS_POSTTRIM_TEMP_READOUT(self, temperature, buf_en):
    Asist_Func.dts_disable(self)
    if buf_en:
        Asist_Func.adcvinbufsel_en(self)
    else:
        Asist_Func.adcvinbufsel_dis(self)
    Asist_Func.rawcode_dis(self)
    Asist_Func.update_chosen_mask(self, 63)  # 6'h3F
    Asist_Func.dts_enable(self)
    data = []  # data = [TDAU temperature, diode temperature , error: T-T* ]
    for diode in range(gen1_diode_num):
        #if Asist_Func.valid_diode_check(self, diode):
        if True:  ###### for debug!!!!
            rawcode = Asist_Func.read_temperature_code(self, diode)
            temperature_measured = rawcode/2 -64
            error = temperature - temperature_measured
            data = [temperature, temperature_measured, error]
            if buf_en:
                self.diodesList[diode].posttrim_gen1_buf_en.append(data)
                print(self.diodesList[diode].posttrim_gen1_buf_en)
            else:
                self.diodesList[diode].posttrim_gen1_buf_dis.append(data)
                print(self.diodesList[diode].posttrim_gen1_buf_dis)
        else:
            print(str(diode) + ' is invalid')

## DTS full accuracy function  ##
def DTS_full_accuracy_func_gen1(self, buf_en):
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_PRETRIM_RAWCODE_READOUT(self, temperature, buf_en)
    Asist_Func.temperature_change(25)
    DTS_trim_gen1(self, buf_en)
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_POSTTRIM_TEMP_READOUT(self, temperature, buf_en)
    Asist_Func.temperature_change(25)


def DTS_ADC_Linearity_check(self):
    Asist_Func.dts_disable(self)
    Asist_Func.adc_vref_select(self, 3)
    Asist_Func.adcvinsel0_select(self, 3)
    Asist_Func.adcvinsel1_select(self, 3)
    Asist_Func.adcdfxextvref_select(self, 0)
    Asist_Func.anadfxinen_select(self, 2)
    print('Apply external voltage reference to Ivref_a ')
    print('Apply external input voltage  to external pin i_ana_dfx_1')
    Asist_Func.oneshot_disable(self)
    Asist_Func.update_diode_mask(self, 0)
    Asist_Func.rawcode_en(self)
    Asist_Func.dts_enable(self)
    voltage_applied = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    data = []
    rawcode = []
    for  i in range(len(voltage_applied)):
        Asist_Func.apply_voltage_i_ana_dfx_1(voltage_applied[i], 0)
        rawcode.append(Asist_Func.read_temperature_code(self, 0))
        data = [voltage_applied[i], rawcode[i]]
        self.adc_linearity_check.append(data)

    self.adc_slope, self.adc_offset = Asist_Func.calculate_slope_and_offset(voltage_applied,rawcode)
    print('slope: ' + str(self.adc_slope))
    print('offset: ' + str(self.adc_offset))

    ##### maybe export graph?


def DTS_CAT_AUTOTRIM_CHECK(self, temperature):
    Asist_Func.dts_disable(self)
    for diode in range(gen1_diode_num):
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, diode)
        Asist_Func.reset_cattrip_fsm(self)
        Asist_Func.dts_enable(self)
        Asist_Func.enable_dts_cattrip_auto_trim_fsm(self)
        while Asist_Func.read_cattrip_fsm_state(self) != 3:
            #continue
            break  ##### for debug!!
        data = []  # data = [temperature cattrip_code cattrip_error]
        code = Asist_Func.read_cattripcode_out(self, diode)
        error = Asist_Func.read_cattripcode_error(self, diode)
        data = [temperature, code, error]
        self.diodesList[diode].catAutoTrimData.append(data)
        Asist_Func.dts_disable(self)

def DTS_CAT_TRIM_GEN1(self, cattrip_temperature):
    _DTS.DTS_cat_trim_rawcode(self, cattrip_temperature)


def DTS_POSTCALIB_CATBLK_TRIP_CHECK(self, temperature_start_point, target_temperature):
    _DTS.DTS_postcalib_catblk_trim_check(self, temperature_start_point, target_temperature)

## DTS full cattrip calib function gen1 ##
def DTS_full_cattrip_calib_func_gen1(self):
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_CAT_AUTOTRIM_CHECK(self, temperature)
    Asist_Func.temperature_change(25)
    for cattrip_temperature in cattripTemperatureListGEn1:
        start_point_temperature = cattrip_temperature - 10
        Asist_Func.temperature_change(start_point_temperature)
        DTS_CAT_TRIM_GEN1(self, cattrip_temperature)
        DTS_POSTCALIB_CATBLK_TRIP_CHECK(self, start_point_temperature, cattrip_temperature)
    Asist_Func.temperature_change(25)


def CATBLK_VREF_VBE_VCOMP_CHECK(self):
    Asist_Func.dts_disable(self)
    cattrip_code = [0, 127]
    for code in cattrip_code:
        Asist_Func.insert_cattrip_code(self, code, 0)  # Set the cattrip trim code=6'b000000
        Asist_Func.program_viewanasigsel(self, 4)  # Select the analog dft mux to out:cattrip comparator vref_min/_max
        Asist_Func.dts_enable(self)
        Asist_Func.measure_analog_func(self, 4)  # Measure vrefmax
        Asist_Func.dts_disable(self)
        Asist_Func.program_viewanasigsel(self, 3)  # Select the analog dft mux to out the cattrip comparator output
        Asist_Func.dts_enable(self)
        Asist_Func.measure_analog_func(self, 3)  # Measure cattrip comparator output
        Asist_Func.dts_disable(self)
    Asist_Func.program_viewanasigsel(self, 5)  # Select the analog dft mux to out the remote diode Vbe
    Asist_Func.dts_enable(self)
    Asist_Func.measure_analog_func(self, 5)  # Measure the comparator vref
    Asist_Func.dts_disable(self)


def DTS_CATTRIP_ALERT_CHK_EXTVBE(self):
    Asist_Func.dts_disable(self)
    print('Apply external voltage Vbe to external vin ana_dfx_1  bump')
    voltages_applied = np.arange(0.4, 0.6+0.002, 0.002)
    Asist_Func.oneshot_disable(self)
    Asist_Func.update_diode_mask(self, 0)
    cattrip_code = 0 ## TBD get the cattrip vref code for 100C
    Asist_Func.insert_cattrip_code(self, cattrip_code, 0)
    Asist_Func.anadfxinen_select(self, 2)
    Asist_Func.program_digital_viewpin_o_digital_1(self, 14)
    Asist_Func.dts_enable(self)
    for voltage in range(len(voltages_applied)):
        Asist_Func.apply_voltage_i_ana_dfx_1(voltage, 0)
        ## TBD if thermtrip alert is generated: break and voltage and compare with the vbe we get form the RD VBE check
        break


def DTS_AVG_SUPLKG_CHECK_ONESHOTMODE(self):
    Asist_Func.dts_disable(self)
    Asist_Func.oneshot_enable(self)
    Asist_Func.program_sleep_timer(self, 1)  # sleep timer of 52u
    Asist_Func.update_diode_mask(self, 1)
    Asist_Func.dts_enable(self)
    print('measure the currents')