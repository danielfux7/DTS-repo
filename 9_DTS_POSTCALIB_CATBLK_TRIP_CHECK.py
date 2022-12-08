## DTS Post calib CATBLK check ##
# Description:
# The function will check the Trim of cattrip of particular DTS:
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

    print('The function will check the Trim of cattrip of particular DTS:')
    print('dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1 \n')
    while 1:
        name = input('Choose the DTS for the test and write the name as showed above \n')
        print(name)

        if type(name) != str:  # check if string
            print('1')
            continue

        if name in ListDTS:  # check the name is correct
            print('2')
            break


    # Program the BG code obtained from the test "BGR_CALIB_STEP2" into the DTS IP
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.bgrtrimcode = Step2TrimValue'
    exec(command)

    # Update diode mask to select the diode that was enabled during calibration (RD7)
    command = 'cpu.cdie.taps.cdie' + name + '.dtsfusecfg.active_diode_mask = 0x1'
    exec(command)

    # Program the cattrip trim value into cattripcode_* for the given target
    # temperature (from previous test,DTS_CAT_AUTOTRIM_CHECK/DTS_CAT_2POINT_AUTOTRIM_CHECK)

    # Program Digital viewpin to monitor cattrip output on o_digital_view[1]
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.viewdigsigsel1 = 0xd'
    exec(command)


    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenable = 1'
    exec(command)


    # For each target temperature, shmoo the temperature in steps of 1C in the range of -10C
    # from the expected target trip temperature



