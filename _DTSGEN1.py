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
    self.NumOfDiode = 6
    self.pre_trim_all_diodes_data = {'dts': [], 'buf_en': [], 'diode': [], 'temperature': [], 'raw_code': []}
    self.slope_offset_all_diodes_data = {'dts': [], 'buf_en': [], 'diode': [], 'slope': [], 'offset': []}
    self.post_trim_all_diodes_data = {'dts': [], 'buf_en': [], 'diode': [], 'temperature': [],
                                      'measured_temperature': [], 'error': []}

    # cattrip data
    self.cat_pre_trim_all_diodes_data = {'dts': [], 'diode': [], 'temperature': [], 'cattrip_code': [], 'error': []}
    self.cat_trim_all_diodes_data = {'dts': [], 'diode': [], 'cat_slope': [], 'cat_offset': [], 'cattrip_code': []}
    self.catblk_post_calib_data = {'dts': [], 'diode': [], 'temperature': [], 'cattrip_temperature': [],
                                   'cat_alert': [], 'status': []}

    self.VBE_check_data_gen1 = {}
    self.PWRON_BGCORE_VBE_VCCBGR_VBG_data = {'bgtrimcode': [], 'BGCORE_VBE1': [], 'VCCBGR': []}
    self.CATBLK_VREF_VBE_VCOMP_CHECK_data = {'dts': [], 'cattrip_code': [], 'Vref_max': [], 'cattrip_comp': [],
                                             'come_vref': []}
    self.DTS_CATTRIP_ALERT_CHK_EXTVBE_data = {'alert_voltage', 'vbe_100_deg', 'voltage_gap'}

    self.sd_adc_linearity_check_data = {'dts': [], 'voltage_applied': [], 'rawcode': []}

    # for i in range(6):
    #     self.diodesList.append(Diode(i))
    self.diodesList = [Diode(i) for i in range(6)]


def BGR_calib_gen1(self, bgrtrimcode):
    Asist_Func.set_any_bg_trim_code(self, bgrtrimcode)


## catblk vref vbe vcomp check ## test 1
# Description:
def DTS_GEN1_TAP_DEFAULT_CHECK(self):
    Asist_Func.dts_enable(self)
    _DTS.DTS_TAP_Default_Check(self)


def PWRON_DTS_RD_VBE_Check(self, temperature):
    _DTS.DTS_RD_VBE_Check(self, temperature)
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


def PWRON_BGCORE_VBE_VCCBGR_VBG(self, bgtrimcode):
    Asist_Func.dts_disable(self)
    Asist_Func.set_any_bg_trim_code(self, bgtrimcode)  # set bgrtrimcode  = 6'b110010 (0x30) =32+16+2 =50 #### verify!!!
    aelf.PWRON_BGCORE_VBE_VCCBGR_VBG_data['bgtrimcode'].append(bgtrimcode)
    Asist_Func.program_viewanasigsel(self, 1)  # Select the analog dft mux to out the BGCORE VBE
    Asist_Func.dts_enable(self)
    vbe1 = Asist_Func.measure_analog_func(self, 1)  # Measure BGCORE VBE1
    self.PWRON_BGCORE_VBE_VCCBGR_VBG_data['BGCORE_VBE1'].append(vbe1)
    Asist_Func.dts_disable(self)
    Asist_Func.program_viewanasigsel(self, 2)  # Select the analog dft mux to out the BGCORE VCCBGR, BGREF(Vbg)
    Asist_Func.dts_enable(self)
    bgr = Asist_Func.measure_analog_func(self, 2)  # Measure VCCBGR
    self.PWRON_BGCORE_VBE_VCCBGR_VBG_data['VCCBGR'].append(bgr)
    Asist_Func.dts_disable(self)

def PWRON_CATBLK_VREF_VBE_VCOMP_CHECK(self): ## no need to use!
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

            # collect data to excel
            self.pre_trim_all_diodes_data['dts'].append(self.name)
            self.pre_trim_all_diodes_data['buf_en'].append(buf_en)
            self.pre_trim_all_diodes_data['diode'].append(diode)
            self.pre_trim_all_diodes_data['temperature'].append(temperature)
            self.pre_trim_all_diodes_data['raw_code'].append(rawcode)

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

            # collect data for the excel
            self.slope_offset_all_diodes_data['dts'].append(self.name)
            self.slope_offset_all_diodes_data['buf_en'].append(buf_en)
            self.slope_offset_all_diodes_data['diode'].append(diode)
            self.slope_offset_all_diodes_data['slope'].append(slope)
            self.slope_offset_all_diodes_data['offset'].append(offset)


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

            # save the data for the excel
            self.post_trim_all_diodes_data['dts'].append(self.name)
            self.post_trim_all_diodes_data['buf_en'].append(buf_en)
            self.post_trim_all_diodes_data['diode'].append(diode)
            self.post_trim_all_diodes_data['temperature'].append(temperature)
            self.post_trim_all_diodes_data['measured_temperature'].append(temperature_measured)
            self.post_trim_all_diodes_data['error'].append(error)

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
    for i in range(len(voltage_applied)):
        Asist_Func.apply_voltage_i_ana_dfx_1(voltage_applied[i], 0)
        rawcode.append(Asist_Func.read_temperature_code(self, 0))
        data = [voltage_applied[i], rawcode[i]]
        self.adc_linearity_check.append(data)

        # save data for excel
        self.sd_adc_linearity_check_data['dts'].append(self.name)
        self.sd_adc_linearity_check_data['voltage_applied'].append(voltage_applied[i])
        self.sd_adc_linearity_check_data['rawcode'].append(rawcode[i])

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

        # save data for excel
        self.cat_pre_trim_all_diodes_data['dts'].append(self.name)
        self.cat_pre_trim_all_diodes_data['diode'].append(diode)
        self.cat_pre_trim_all_diodes_data['temperature'].append(temperature)
        self.cat_pre_trim_all_diodes_data['cattrip_code'].append(code)
        self.cat_pre_trim_all_diodes_data['error'].append(error)


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
    DTS_CAT_TRIM_GEN1(self, 20)  ####### need to modify the tem to 80
    for cattrip_temperature in cattripTemperatureListGEn1:
        start_point_temperature = cattrip_temperature - 10
        Asist_Func.temperature_change(start_point_temperature)
        DTS_POSTCALIB_CATBLK_TRIP_CHECK(self, start_point_temperature, cattrip_temperature)
    Asist_Func.temperature_change(25)


def CATBLK_VREF_VBE_VCOMP_CHECK(self):
    Asist_Func.dts_disable(self)
    cattrip_code = [0, 63]
    for code in cattrip_code:
        Asist_Func.insert_cattrip_code(self, code, 0)  # Set the cattrip trim code=6'b000000 for diode 0(can modify it)
        self.CATBLK_VREF_VBE_VCOMP_CHECK_data['dts'].append(self.name)
        self.CATBLK_VREF_VBE_VCOMP_CHECK_data['cattrip_code'].append(code)

        Asist_Func.program_viewanasigsel(self, 4)  # Select the analog dft mux to out:cattrip comparator vref_min/_max
        Asist_Func.dts_enable(self)
        vrefmax = Asist_Func.measure_analog_func(self, 4)  # Measure vrefmax
        self.CATBLK_VREF_VBE_VCOMP_CHECK_data['Vref_max'].append(vrefmax)
        Asist_Func.dts_disable(self)

        Asist_Func.program_viewanasigsel(self, 3)  # Select the analog dft mux to out the cattrip comparator output
        Asist_Func.dts_enable(self)
        comp_out = Asist_Func.measure_analog_func(self, 3)  # Measure cattrip comparator output
        self.CATBLK_VREF_VBE_VCOMP_CHECK_data['cattrip_comp'].append(comp_out)
        Asist_Func.dts_disable(self)

        Asist_Func.program_viewanasigsel(self, 5)  # Select the analog dft mux to out the comparator vref
        Asist_Func.dts_enable(self)
        come_vref = Asist_Func.measure_analog_func(self, 5)  # Measure the comparator vref
        self.CATBLK_VREF_VBE_VCOMP_CHECK_data['come_vref'].append(come_vref)
        Asist_Func.dts_disable(self)


def DTS_CATTRIP_ALERT_CHK_EXTVBE(self):
    Asist_Func.dts_disable(self)
    print('Apply external voltage Vbe to external vin ana_dfx_1  bump')
    voltages_applied = np.arange(0.4, 0.6+0.002, 0.002)
    Asist_Func.oneshot_disable(self)
    Asist_Func.update_diode_mask(self, 0)
    vbe1_100_deg = 0 ## TBD get the vbe voltage for 100C of diode 0
    Asist_Func.insert_cattrip_code(self, cattrip_code, 0)
    Asist_Func.anadfxinen_select(self, 2)
    Asist_Func.program_digital_viewpin_o_digital_1(self, 14)
    Asist_Func.dts_enable(self)
    for voltage in range(len(voltages_applied)):
        Asist_Func.apply_voltage_i_ana_dfx_1(voltage, 0)
        ## TBD if thermtrip alert is generated: break and voltage and compare with the vbe we get form the RD VBE check
        if Asist_Func.measure_digital_func(self, 0xd):
            self.DTS_CATTRIP_ALERT_CHK_EXTVBE_data['alert_voltage'].append(voltage)
            self.DTS_CATTRIP_ALERT_CHK_EXTVBE_data['vbe_100_deg'].append(vbe1_100_deg)
            self.DTS_CATTRIP_ALERT_CHK_EXTVBE_data['voltage_gap'].append(voltage-vbe1_100_deg)
            break


def DTS_AVG_SUPLKG_CHECK_ONESHOTMODE(self):
    Asist_Func.dts_disable(self)
    Asist_Func.oneshot_enable(self)
    Asist_Func.program_sleep_timer(self, 1)  # sleep timer of 52u
    Asist_Func.update_diode_mask(self, 1)
    Asist_Func.dts_enable(self)
    print('measure the currents')