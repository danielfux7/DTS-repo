## DTS POST TRIM TEMP READOUT ##
# Description:
# The function will get read the temperatures from all the diodes of particular DTS:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
# TBD - ADD DESCRIPTION

import namednodes as _namednodes
from config import *


try:
    _sv = _namednodes.sv.get_manager(["socket"])
except:
    print("WARNING: Socket discovery failed to find any sockets")

try:
    cpu = _sv.socket.get_all()[0]
except:
    print("WARNING: Your PythonSV doesn't seem to have the cpu component loaded. Some scripts may fail due to this.")


# Constants #
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0' , 'dts_ccf1', 'dts_gt0', 'dts_gt1']
VinADC = 0.77
VrefADC = 0.93
MeasurementsNum = 100

if __name__ == '__main__':

    print('The function will get BG TRIM - STEP 1 on of the following DTSs:')
    print('dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1 \n')
    while 1:
        name = input('Choose the DTS for trim and write the name as showed above \n')
        print(name)

        if type(name) != str:  # check if string
            print('1')
            continue

        if name in ListDTS:  # check the name is correct
            print('2')
            break


    # Program the BG code obtained from the test "BGR_CALIB_STEP2" into the DTS IP
    command = 'cdie.taps.cdie_' + name + '.dtsfusecfg.bgrtrimcode = Step2TrimValue'
    exec(command)

    # Update diode mask to select all the diodes that were calibrated and needed for temperature measurement (RD0 to  RD16)
    command = 'cpu.cdie.taps.cdie' + name + '.dtsfusecfg.active_diode_mask = 0xffff'
    exec(command)

    # "Offset & slope from pre trim test  should be updated in CR for all calibrated diodes
    # (Calibration points -10C & 100C)" TBD -check if need to do something here

    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenable = 1'
    exec(command)

    # Wait for DTS power up and all diode temperature conversion time- 300us TBD- check if need to something with
    # delay, according to DIma I dont need

    # Read rawcode for the selectied diode via registers when temperature valid
    # for that particular diode is 1 through TAP.



