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

def rawcode_read(self,diode):
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtstemperature_' + str(diode)
    rawcode = eval(command)
    return int(rawcode)