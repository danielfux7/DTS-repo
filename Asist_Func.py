import namednodes as _namednodes
import pandas as pd
import numpy as np
from config import *

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
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1']
OSRmodes = ['256_avgdis', '512_avgdis', '1024_avgdis', '2048_avgdis',
            '256_avgen', '512_avgen', '1024_avgen', '2048_avgen']

OSRmodesNum = 8
VinADC = 0.77
VrefADC = 0.93
MeasurementsNum = 5

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

Taps = ['dtsfusecfg', 'tapconfig', 'tapstatus']

def update_chosen_mask(self, mask):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.active_diode_mask =' + str(mask)
    exec(command)

def update_diode_mask(self, diodeNum):
    diodeMask = pow(2, diodeNum)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.active_diode_mask =' + str(diodeMask)
    exec(command)

def program_bg_code(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrtrimcode =' + str(self.Step2TrimValue)
    exec(command)

def oneshot_disable(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0x0'
    exec(command)

def oneshot_enable(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0x1'
    exec(command)

def dts_enable(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 1'
    exec(command)

def dts_disable(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 0'
    exec(command)


def all_dts_disable():
    for dts in ListDTS:
        command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenable = 0'
        exec(command)


def all_dts_enable():
    for dts in ListDTS:
        command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenableovrd = 1'
        exec(command)
        command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.dtsenable = 1'
        exec(command)


def valid_diode_check(self, diode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtstemperaturevalid_' + str(diode)
    valid = eval(command)
    return int(valid)


def rawcode_read(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.adcrawcode'
    rawcode = eval(command)
    return int(rawcode)


def calculate_slope_and_offset(x, y):
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
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cattripcode_' + str(diode) + '=' + str(cattripcode)
    exec(command)


def insert_slope_offset_to_diode(self, diode, slope, offset):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.slope_' + str(diode) + '=' + str(slope)
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.offset_' + str(diode) + '=' + str(offset)
    exec(command)
    self.diodesList[diode].slope = slope
    self.diodesList[diode].offset = offset


def update_osr_mode(self, avgen, mode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.adc_avgen=' + str(avgen)
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.osr=' + str(mode)
    exec(command)

def read_temperature_code(self, diode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtstemperature_' + str(diode)
    tempCode = eval(command)
    return int(tempCode)

def diode_sel_ovr_en(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_en=1'
    exec(command)

def diode_sel_ovr_val(self, diode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_val=' + str(diode)
    exec(command)


def cat_alert_clear(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cat_alert_clr=1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.cat_alert_clr=0'
    exec(command)

def reset_cattrip_fsm(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimrstovrd=1'
    exec(command)

def release_cattrip_fsm_reset(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimrstovrd=0'
    exec(command)

def enable_dts_cattrip_auto_trim_fsm(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimen=1'
    exec(command)

def program_digital_viewpin_o_digital_0(self, selector):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.viewdigsigsel0=' + str(selector)
    exec(command)

def program_digital_viewpin_o_digital_1(self, selector):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.viewdigsigsel1=' + str(selector)
    exec(command)

def read_cattrip_fsm_state(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattripfsmstate'
    cattripFsmState = eval(command)
    return int(cattripFsmState)

def read_cattripcode_out(self,diode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattripcode_out_' + str(diode)
    cattripCode = eval(command)
    return int(cattripCode)

def enable_trim_neg_temperature(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.cattriptrimen_negtemp=1'
    exec(command)


def cattrip_alert(self):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.cattrip_alert'
    cattripAllert = eval(command)
    return int(cattripAllert)


