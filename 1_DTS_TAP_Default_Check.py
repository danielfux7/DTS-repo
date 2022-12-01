## DTS TAP Defualt Check ##
# Description:
# The function will will check TAPs on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
# The function will take


import namednodes as _namednodes

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
    print('The function will do TAPs check on of the following DTSs:')
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

    # DTS power on and enable all the powergoods
    # command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.digitalpwrgoodovr=1'
    # exec(command)
    # command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.digitalpwrgoodval=1'
    # exec(command)
    #
    # exec('cpu.cdie.taps.cdie_pgramp1.pgramptapstatus.aonpwrgood = 0x1')
    # exec('cpu.cdie.taps.cdie_pgramp2.pgramptapstatus.aonpwrgood = 0x1')



    print('finish TAPs check')