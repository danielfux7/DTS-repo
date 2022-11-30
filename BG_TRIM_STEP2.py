## BG TRIM STEP 2 ##
# Description:
# The function will get BG TRIM on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1

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
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1']
VinADC = 0.77
VrefADC = 0.93
MeasurementsNum = 100

if __name__ == '__main__':
    print('The function will get BG TRIM - STEP 2 on of the following DTSs:')
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

    # a. program 1.2V LDO reference selection mux to take lvr ref as reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x1'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.8V as input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 4'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 2'
    exec(command)

    # c. Program vref_ldo to take internal BG reference as input
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 0x0'
    exec(command)

    # d. Program vref_ldo resistance divider to take 0.7V as input reference voltage – functional scenario
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg6_inst.vrefldo_vref_range_sel = 2'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.adc_vrefldo_out_sel = 0x1'
    exec(command)

    # e. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # Take Vref_ldo output as reference voltage for ADC & Supply_buffer which is the case of regular
    # functional mode operation
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg15_inst.adcvrefbufsel = 0x1'
    exec(command)

    # config ADC - Value must be same as chosen in Step 1 procedure
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg14_inst.adcvinsel0 = 3'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name +'.tapconfig.anadfxinen = 3'
    exec(command)

    # Select diode RD7 with ovrd and ovrd en (from test plan) not sure its needed .....
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.remote_diode_sel_ovr_en = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.remote_diode_sel_ovr_val = 0'
    exec(command)

    # Disable oneshot mode(from test plan) not sure its needed .....
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.oneshotmodeen = 0'
    exec(command)

    ## 3-6 Start trimming BG trim bits, took the recipe from test plan

    # Set the BG Trim lower and higher limit codes via register ,the values are not make sense nee to check!! TBD
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.bgrtrimhighlimit = 30'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.bgrtrimlowlimit = 5'
    exec(command)

    # Set the BG Trim start point such that vref_ldo output <0.9V. Update timer to wait for 4.6us for every BG code
    # increment/decrement before starting ADC conversion. This gives enough time for analog to settle.
    ## TBD how to to make sure there is a waiting time between the increment/decrement
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.bgrtrimrstval = 18'
    exec(command)

    # Enable BG Trim mode
    command = 'cdie.taps.cdie_' + name + '.tapconfig.bgtrim_mode = 1'
    exec(command)

    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.dtsfusecfg.dtsenable = 1'
    exec(command)

    # Keep polling the BGTRIM Done register till it becomes 1
    command = 'cpu.cdie.taps.cdie_' + name + '.tapstatus.bgtrim_done'
    done = 0

    while done == 0:
        done = eval(command)
        done = 1 # just for debug

    # Read the values of BGTRIM FSM state and ensure that BGTRIM is completed without any error
    command = 'cpu.cdie.taps.cdie_' + name + '.tapstatus.bgtrimfsmstate'
    BGTrimStateFsm = eval(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.tapstatus.bgtrimerror'
    error = eval(command)

    print(BGTrimStateFsm)

    if error == 1:
        print('calib error')

    command = 'cpu.cdie.taps.cdie_' + name + '.tapstatus.bgtrimcode_calib'
    BGTrimCalib = eval(command)
    print('bgtrimcode calib:')
    print(BGTrimCalib)

    print('STEP2 finished')




  #  SumBGRCode = 0
   #AvgStep1Code = 0  #### TBD - insert the code from the register
    #command = '# TBD - how to configure to 10 bits code?'
    #exec(command)

    # MeasureBGRCommand = ''  # TBD - check what is the command for getting bgrtirmcode
    # IncrementBgrtrim = ''  # TBD - check what is the command for increment in one step bgrtirmcode
    # DecrementBgrtrim = ''  # TBD - check what is the command for decrement in one step bgrtirmcode
    #
    # # First, we will check if we need to increase or to decrease the bgtrimcode in order to get to the right val
    # for i in range(MeasurementsNum):
    #     SumBGRCode += eval(MeasureBGRCommand)
    #
    # AverageCode = SumBGRCode / MeasurementsNum
    #
    # if AverageCode > AvgStep1Code:
    #     while AverageCode > AvgStep1Code:
    #         exec(DecrementBgrtrim)
    #         # time.sleep(1) - TBD check what is right command
    #         for i in range(MeasurementsNum):
    #             SumBGRCode += eval(MeasureBGRCommand)
    #
    #         AverageCode = SumBGRCode / MeasurementsNum
    #     exec(IncrementBgrtrim)
    #     # time.sleep(1) - TBD check what is right command
    #
    # else:
    #     while AverageCode < AvgStep1Code:
    #         exec(IncrementBgrtrim)
    #         # time.sleep(1) - TBD check what is right command
    #         for i in range(MeasurementsNum):
    #             SumBGRCode += eval(MeasureBGRCommand)
    #
    #         AverageCode = SumBGRCode / MeasurementsNum





