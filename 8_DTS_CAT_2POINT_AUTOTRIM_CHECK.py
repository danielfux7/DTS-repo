## DTS Cat 2 Point auto Teim check ##
# Description:
# The function will Trim the cattrrip s of particular DTS:
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

    print('The function will Trim the cattrrip s of particular DTS:')
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
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.bgrtrimcode = Step2TrimValue'
    exec(command)

    # Select required diode  RD(0-11)with ovrd and ovrd en

    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenable = 1'
    exec(command)


    # Clear cat alert - by writing "cat_alert_clr" to 1 and then to 0 in two consecutive writes
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.cat_alert_clr = 0x1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.cat_alert_clr = 0x0'
    exec(command)

    # Reset cattrip FSM by writing "cattriptrimrstovrd" to 1
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.cattriptrimrstovrd = 0x1'
    exec(command)


    # Enable DTS catrip auto trim FSM
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.cattriptrimen = 0x1'
    exec(command)

    # Release cattrip FSM reset  by writing "cattriptrimrstovrd" to 0
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.cattriptrimrstovrd = 0x0'
    exec(command)


    # Program Digital viewpin to monitor cattrip output on o_digital_view[1]
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.viewdigsigsel1 = 0xd'
    exec(command)


    # Monitor cattrip trim FSM  on TAP status( wait for  cattripfsmstate  -> 2'b11 )
    FSMcattripState=0
    command = 'cpu.cdie.taps.cdie_' + name + '.tapstatus.cattripfsmstate'
    #FSMcattripState = 3 # FOR DEBUG
    while FSMcattripState != 3:
        FSMcattripState = eval(command)

    # Once the trimming is completed read the TAP  status register for trim code
    # which is updated in the cattripcode_*[0-15]


