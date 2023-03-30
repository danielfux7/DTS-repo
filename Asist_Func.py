import namednodes as _namednodes
import pandas as pd
import numpy as np
from config import *
import pickle
import time

try:
    _sv = _namednodes.sv.get_manager(["socket"])
except:
    print("WARNING: Socket discovery failed to find any sockets")

try:
    cpu = _sv.socket.get_all()[0]
except:
    print(
        "WARNING: Your PythonSV doesn't seem to have the cpu component loaded. Some scripts may fail due to this.")

# Constants #
Mega = 1000000
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1']
listGEN1DTS=['par_sa_pma0_core0_dts0', 'par_sa_pma0_core1_dts0', 'par_sa_pma1_core0_dts0',
             'par_sa_pma1_core1_dts0', 'atom_lpc']
ListAllDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1',
              'par_sa_pma0_core0_dts0', 'par_sa_pma0_core1_dts0', 'par_sa_pma1_core0_dts0',
              'par_sa_pma1_core1_dts0', 'atom_lpc']

DTS_dict = {'dts0_aon': 0, 'dts1': 0, 'dts2': 0, 'dts3': 0, 'dts_ccf0': 0, 'dts_ccf1': 0, 'dts_gt0': 0, 'dts_gt1': 0,
              'par_sa_pma0_core0_dts0': 0, 'par_sa_pma0_core1_dts0': 0, 'par_sa_pma1_core0_dts0': 0,
              'par_sa_pma1_core1_dts0': 0, 'atom_lpc': 0}

OSRmodes = ['256_avgdis', '512_avgdis', '1024_avgdis', '2048_avgdis',
            '256_avgen', '512_avgen', '1024_avgen', '2048_avgen']
FrequenciesDict = {25: 2, 50: 0, 100: 1}
FrequenciesList = [25, 50, 100]
temperatureList = [10, 30, 50, 70, 90]
cattripTemperatureList = [80, 90, 95, 100, 105, 110, 115, 125]
cattripTemperatureListGEn1 = [80, 100, 125]
anaPwrSeqSignalList = ['power_gate_enable', 'BGR_enable', 'LDO1p2V_enabled', 'ADC_sup_buf_enable',
                       'ADC_sup_buf_enable_delayed']
anaPwrSeqSignalDict = {'power_gate_enable': 8, 'BGR_enable': 0, 'LDO1p2V_enabled': 1, 'ADC_sup_buf_enable': 2,
                       'ADC_sup_buf_enable_delayed': 15}

OSRmodesNum = 8
VinADC = 0.77
VrefADC = 0.93
primaryCounter = 1024
MeasurementsNum = 5
NumNsAllert = 4
gen1_diode_num = 6

DiodeNum = {
    "dts0_aon": 1,
    "dts1": 9,
    "dts2": 9,
    "dts3": 9,
    "dts_ccf0": 2,
    "dts_ccf1": 2,
    "dts_gt0": 6,
    "dts_gt1": 6,
}

Taps = ['dtsfusecfg', 'tapconfig', 'tapstatus', 'CRI', 'CRI_vs_TAPs', 'dtstapcfgfuse']


def create_new_path_for_func(path, func_name, dts_name):
    new_path = path + '\\' + str(func_name) + '_' + dts_name + '.xlsx'
    print(new_path)
    return new_path


def convert_array_to_dict(arr, title_names):
    if len(arr) == 0:
        print('Error! array is empty')
        return
    new_dict = {}
    curr_list =[]
    for i in range(len(arr[0])):
        curr_list = [item[i] for item in arr]
        new_dict[title_names[i]] = curr_list
    print(new_dict)
    return new_dict

def create_excel_file_for_chosen_func(self, func_name, dict_for_excel):
    path = create_new_path_for_func(self.path, func_name, self.name)
    df = pd.DataFrame.from_dict(dict_for_excel)
    df.to_excel(path)


def update_chosen_mask(self, mask):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.active_diode_mask =' + str(mask)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.active_diode_mask =' + str(mask)
    exec(command)


def update_diode_mask(self, diodeNum):
    diodeMask = pow(2, diodeNum)
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.active_diode_mask =' + str(diodeMask)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.active_diode_mask =' + str(diodeMask)
    exec(command)


def program_bg_code(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrtrimcode =' + str(self.Step2TrimValue)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgrtrimcode =' + str(self.Step2TrimValue)
    exec(command)


def set_any_bg_trim_code(self, bgtrimcode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrtrimcode =' + str(bgtrimcode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgrtrimcode =' + str(bgtrimcode)
    exec(command)


def set_any_tc(self, tc):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrtc =' + str(tc)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgrtc =' + str(tc)
    exec(command)


def set_any_bgradj(self, bgradj):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgradj =' + str(bgradj)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgradj =' + str(bgradj)
    exec(command)


def oneshot_disable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0x0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.oneshotmodeen = 0x0'
    exec(command)


def oneshot_enable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0x1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.oneshotmodeen = 0x1'
    exec(command)

def dts_enable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 1'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtsenable = 1'
        exec(command)

def dts_disable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 0'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtsenable = 0'
        exec(command)

def all_dts_disable():
    for dts in ListAllDTS:
        if dts != 'atom_lpc':
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenableovrd = 1'
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenable = 0'
            exec(command)
        else:
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtstapcfgfuse.dtsenableovrd = 1'
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtstapcfgfuse.dtsenable = 0'
            exec(command)


def all_dts_enable(self):
    for dts in ListAllDTS:
        if dts != 'atom_lpc':
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenableovrd = 1'
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenable = 1'
            exec(command)
        else:
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtstapcfgfuse.dtsenableovrd = 1'
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtstapcfgfuse.dtsenable = 1'
            exec(command)


def valid_diode_check(self, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtstemperaturevalid_' + str(diode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtstemperaturevalid_' + str(diode)
    valid = eval(command)
    return int(valid)


def rawcode_read(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.adcrawcode'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.adcrawcode'
    rawcode = eval(command)
    return int(rawcode)


def bgtrim_done(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrim_done'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.bgtrim_done'
    bgtrim_done = eval(command)
    return int(bgtrim_done)


def bgtrim_fsm_state(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimfsmstate'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.bgtrimfsmstate'
    bgtrimfsmstate = eval(command)
    return int(bgtrimfsmstate)


def bgtrim_error(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimerror'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.bgtrimerror'
    bgtrimerror = eval(command)
    return int(bgtrimerror)


def bgtrimcode_calib(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimcode_calib'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.bgtrimcode_calib'
    bgtrimcode_calib = eval(command)
    return int(bgtrimcode_calib)


def rawcode_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.rawcode_en = 0x1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.rawcode_en = 0x1'
    exec(command)


def rawcode_dis(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.rawcode_en = 0x0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.rawcode_en = 0x0'
    exec(command)


def calculate_slope_and_offset(x, y):
    coefficients = np.polyfit(x, y, 1)
    slope = round(coefficients[0])
    offset = round(coefficients[1])
    return slope, offset


def calculate_slope_and_offset_gen1(x, y):
    coefficients = np.polyfit(x, y, 1)
    slope = round(coefficients[0])
    offset = round(coefficients[1])
    return slope, offset


def insert_cat_slope_offset_to_diode(self, diode, slope, offset):
    self.diodesList[diode].catSlope = slope
    self.diodesList[diode].catOffset = offset


def convert_temperature_to_rawcode(temperature, slope, offset):
    rawcode = round((temperature - offset) / slope)
    return rawcode


def insert_cattrip_code(self, cattripcode, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cattripcode_' + str(diode) + '=' + str(cattripcode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.cattripcode_' + str(diode) + '=' + str(cattripcode)
    exec(command)


def insert_slope_offset_to_diode(self, diode, slope, offset):
    slope_fuse = int(-(slope * pow(2, 12)))
    offset_fuse = int(offset * 2)
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.slope_' + str(diode) + '=' + str(slope_fuse)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.offset_' + str(diode) + '=' + str(offset_fuse)
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.slope_' + str(diode) + '=' + str(slope_fuse)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.offset_' + str(diode) + '=' + str(offset_fuse)
        exec(command)

    self.diodesList[diode].slope = slope
    self.diodesList[diode].offset = offset


def reinsert_calculated_existed_slope_offset(self, diode):
    slope = self.diodesList[diode].slope
    offset = self.diodesList[diode].offset
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.slope_' + str(diode) + '=' + str(slope)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.offset_' + str(diode) + '=' + str(offset)
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.slope_' + str(diode) + '=' + str(slope)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.offset_' + str(diode) + '=' + str(offset)
        exec(command)


def update_osr_mode(self, avgen, mode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_avgen=' + str(avgen)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.osr=' + str(mode)
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_avgen=' + str(avgen)
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.osr=' + str(mode)
        exec(command)


def read_temperature_code(self, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtstemperature_' + str(diode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtstemperature_' + str(diode)
    tempCode = eval(command)
    temperature_in_degrees = int(tempCode)/2 - 64
    return temperature_in_degrees


def diode_sel_ovr_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_en=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.remote_diode_sel_ovr_en=1'
    exec(command)


def diode_sel_ovr_val(self, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_val=' + str(diode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.remote_diode_sel_ovr_val=' + str(diode)
    exec(command)

def cat_alert_clear(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cat_alert_clr=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cat_alert_clr=0'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.cat_alert_clr=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.cat_alert_clr=0'
        exec(command)

def reset_cattrip_fsm(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimrstovrd=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.cattriptrimrstovrd=1'
    exec(command)

def release_cattrip_fsm_reset(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimrstovrd=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.cattriptrimrstovrd=0'
    exec(command)

def enable_dts_cattrip_auto_trim_fsm(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimen=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.cattriptrimen=1'
    exec(command)

def program_digital_viewpin_o_digital_0(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.viewdigsigsel0=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.viewdigsigsel0=' + str(selector)
    exec(command)

def program_digital_viewpin_o_digital_1(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.viewdigsigsel1=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.viewdigsigsel1=' + str(selector)
    exec(command)

def program_viewanasigsel(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.viewanasigsel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.viewanasigsel=' + str(selector)
    exec(command)

def read_cattrip_fsm_state(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattripfsmstate'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.cattripfsmstate'
    cattripFsmState = eval(command)
    return int(cattripFsmState)


def read_cattripcode_out(self, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattripcode_out_' + str(diode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.cattripcode_out_' + str(diode)
    cattripCode = eval(command)
    return int(cattripCode)


def read_cattripcode_error(self, diode):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattripcode_error_' + str(diode)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.cattripcode_error_' + str(diode)
    errorCode = eval(command)
    return int(errorCode)


def enable_trim_neg_temperature(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimen_negtemp=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.cattriptrimen_negtemp=1'
    exec(command)


def cattrip_alert(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattrip_alert'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.cattrip_alert'
    cattripAllert = eval(command)
    return int(cattripAllert)


def program_bg_wait(self, waitDelay):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrwaitdelay=' + str(waitDelay)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgrwaitdelay=' + str(waitDelay)
    exec(command)


def read_mean_max_min_rawcode_for_diode(self, readNum):
    pass


def program_sleep_timer(self, sleepTime):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.sleeptimer=' + str(sleepTime)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.sleeptimer=' + str(sleepTime)
    exec(command)


def enable_dynamic_update(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.enable_dynamic_update=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.enable_dynamic_update=1'
    exec(command)


def disable_dynamic_update(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.enable_dynamic_update=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.enable_dynamic_update=0'
    exec(command)


def program_adc_clock_freq(self, freq):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsadcclkdiv=' + str(freq)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtsadcclkdiv=' + str(freq)
    exec(command)


def dithering_enable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dithering_enable=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dithering_enable=1'
    exec(command)

def dithering_disable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dithering_enable=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dithering_enable=0'
    exec(command)


def dtd_alert(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.dtd_alert'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.dtd_alert'
    dtdAllert = eval(command)
    return int(dtdAllert)

def dtd_ns_alert(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.dtd_ns_alert'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapstatus.dtd_ns_alert'
    dtdnsAllert = eval(command)
    return int(dtdnsAllert)

def dtd_ns_alert_threshold_direction_insert(self, threshold, direction):
    T = (threshold + 64) * 2
    for i in range(NumNsAllert):
        if self.name != 'atom_lpc':
            command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_nsalert_thr_' + str(i) + '=' + str(T)
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_nsalert_' + str(i) + '_dir=' + str(direction)
            exec(command)
        else:
            command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_nsalert_thr_' + str(i) + '=' + str(T)
            exec(command)
            command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_nsalert_' + str(i) + '_dir=' + str(direction)
            exec(command)


def dtd_sticky_thr_high(self, highLimit):
    T = (highLimit + 64) * 2
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_sticky_thr_h=' + str(T)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_sticky_thr_h=' + str(T)
    exec(command)


def dtd_sticky_thr_low(self, lowLimit):
    T = (lowLimit + 64) * 2
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_sticky_thr_l=' + str(T)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_sticky_thr_l=' + str(T)
    exec(command)


def clear_sticky_alert(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_sticky_alert_clr=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtd_sticky_alert_clr=0'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_sticky_alert_clr=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.dtd_sticky_alert_clr=0'
        exec(command)


def ldo1p2_vref_range_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.ldo1p2_vref_range_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.ldo1p2_vref_range_sel=' + str(selector)
    exec(command)


def vrefldo_vref_range_sel(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.vrefldo_vref_range_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.vrefldo_vref_range_sel=' + str(selector)
    exec(command)


def adc_vrefldo_out_sel(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_vrefldo_out_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_vrefldo_out_sel=' + str(selector)
    exec(command)


def ldo1p2_out_sel(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.ldo1p2_out_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.ldo1p2_out_sel=' + str(selector)
    exec(command)


def ldo1p2_ext_vref_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.ldo1p2_ext_vref_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.ldo1p2_ext_vref_sel=' + str(selector)
    exec(command)


def adc_vref_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvrefsel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvrefsel=' + str(selector)
    exec(command)


def adc_vrefldo_ext_vref_sel(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_vrefldo_ext_vref_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_vrefldo_ext_vref_sel=' + str(selector)
    exec(command)


def adc_vref_buf_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvrefbufsel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvrefbufsel=' + str(selector)
    exec(command)


def adc_supply_buf_vref_ext_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_supply_buf_vref_ext_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_supply_buf_vref_ext_sel=' + str(selector)
    exec(command)


def adc_supply_buf_out_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_supply_buf_out_sel=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_supply_buf_out_sel=' + str(selector)
    exec(command)


def adcvinsel0_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvinsel0=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvinsel0=' + str(selector)
    exec(command)


def adcvinsel1_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvinsel1=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvinsel1=' + str(selector)
    exec(command)


def adcvinbufsel_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvinbufsel=3'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvinbufsel=3'
    exec(command)


def adcvinbufsel_dis(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adcvinbufsel=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adcvinbufsel=0'
    exec(command)

def adcdfxextvref_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.adcdfxextvref=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.adcdfxextvref=' + str(selector)
    exec(command)


def anadfxinen_select(self, selector):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.anadfxinen=' + str(selector)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.anadfxinen=' + str(selector)
    exec(command)


def aon_enable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.dtsaonovrd=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.dtsaonovrdval=1'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.dtsaonovrd=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.dtsaonovrdval=1'
        exec(command)


def aon_disable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.dtsaonovrd=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.dtsaonovrdval=0'
        exec(command)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.dtsaonovrd=1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.dtsaonovrdval=0'
        exec(command)


def bgtrimtarget(self, bgtrimtarget):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgtrimtarget=' + str(bgtrimtarget)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgtrimtarget=' + str(bgtrimtarget)
    exec(command)


def bgrtrimlowlimit(self, bgrtrimlowlimit):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimlowlimit=' + str(bgrtrimlowlimit)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgrtrimlowlimit=' + str(bgrtrimlowlimit)
    exec(command)


def bgrtrimhighlimit(self, bgrtrimhighlimit):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimhighlimit=' + str(bgrtrimhighlimit)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgrtrimhighlimit=' + str(bgrtrimhighlimit)
    exec(command)


def bgrtrimrstval(self, bgrtrimrstval):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimrstval=' + str(bgrtrimrstval)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgrtrimrstval=' + str(bgrtrimrstval)
    exec(command)


def bgtrim_mode_enable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgtrim_mode=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgtrim_mode=1'
    exec(command)


def bgtrim_mode_disable(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgtrim_mode=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapconfig.bgtrim_mode=0'
    exec(command)


def lvrrref_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.lvrref_en=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.lvrref_en=1'
    exec(command)


def lvrrref_dis(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.lvrref_en=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.lvrref_en=0'
    exec(command)


def adc_az_offset_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_az_offset_en=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_az_offset_en=1'
    exec(command)


def adc_az_offset_dis(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_az_offset_en=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.adc_az_offset_en=0'
    exec(command)


def fusa_en(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.fusa_en=1'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.fusa_en=1'
    exec(command)


def fusa_dis(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.fusa_en=0'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.fusa_en=0'
    exec(command)


def fusa_max_thresh(self, max_thresh):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.fusa_max_thresh=' + str(max_thresh)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.fusa_max_thresh=' + str(max_thresh)
    exec(command)


def fusa_min_thresh(self, min_thresh):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.fusa_min_thresh=' + str(min_thresh)
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.fusa_min_thresh=' + str(min_thresh)
    exec(command)


def bgr_out_of_spec(self):
    if self.name != 'atom_lpc':
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgr_out_of_spec'
    else:
        command = 'cpu.cdie.taps.cdie_' + self.name + '.dtstapcfgfuse.bgr_out_of_spec'
    out_of_spec = eval(command)
    return int(out_of_spec)


# In this function, you need to implement the measurement method according to your measurement device
def measure_analog_func(self, analog_view_num):
    print('measure voltage with data logger and return the value')  # need to implement the Evatar
    return 0.5  #### for debug!!

# In this function, you need to implement the measurement method according to your measurement device
def measure_digital_func(self, digital_view_num):
    input() # need to implement the Evatar


# In this function, you need to implement the voltage implementation method according to your device
def apply_voltage_i_ana_dfx_1(voltage, frequency):
    print('The new voltage is ' + str(voltage))  # need to implement the Evatar
    if frequency:
        print('insert sin vin with amplitude of voltage/2 and the given frequency')
    else:
        print('apply DC voltage')



# In this function, you need to implement the temperature implementation method according to your device
def temperature_change(temperature):
    print('The new temperatue is ' + str(temperature))