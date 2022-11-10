## BG TRIM STEP 2 ##
# Description:
# The function will get BG TRIM on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1

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
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x0'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.8V as input reference voltage
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 100'
    exec(command)
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 10'
    exec(command)

    # c. Program vref_ldo to take internal BG reference as input
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 0x0'
    exec(command)

    # d. Program vref_ldo resistance divider to take 0.7V as input reference voltage – functional scenario
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg6_inst.vrefldo_vref_range_sel = 10'
    exec(command)
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.adc_vrefldo_out_sel = 0x1'
    exec(command)

    # e. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # Take Vref_ldo output as reference voltage for ADC & Supply_buffer which is the case of regular
    # functional mode operation
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg15_inst.adcvrefbufsel = 0x1'
    exec(command)

    # config ADC - Value must be same as chosen in Step 1 procedure
    command = 'cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg14_inst.adcvinsel0 = 11'
    exec(command)
    command = 'cdie.taps.cdie_' + name '.tapconfig.anadfxinen = 11'
    exec(command)

    SumBGRCode = 0
    AvgStep1Code = 0  #### TBD - insert the code from the register
    command = '# TBD - how to configure to 10 bits code?'
    exec(command)

    MeasureBGRCommand = ''  # TBD - check what is the command for getting bgrtirmcode
    IncrementBgrtrim = ''  # TBD - check what is the command for increment in one step bgrtirmcode
    DecrementBgrtrim = ''  # TBD - check what is the command for decrement in one step bgrtirmcode

    # First, we will check if we need to increase or to decrease the bgtrimcode in order to get to the right val
    for i in range(MeasurementsNum):
        SumBGRCode += eval(MeasureBGRCommand)

    AverageCode = SumBGRCode / MeasurementsNum

    if AverageCode > AvgStep1Code:
        while AverageCode > AvgStep1Code:
            exec(DecrementBgrtrim)
            # time.sleep(1) - TBD check what is right command
            for i in range(MeasurementsNum):
                SumBGRCode += eval(MeasureBGRCommand)

            AverageCode = SumBGRCode / MeasurementsNum
        exec(IncrementBgrtrim)
        # time.sleep(1) - TBD check what is right command

    else:
        while AverageCode < AvgStep1Code:
            exec(IncrementBgrtrim)
            # time.sleep(1) - TBD check what is right command
            for i in range(MeasurementsNum):
                SumBGRCode += eval(MeasureBGRCommand)

            AverageCode = SumBGRCode / MeasurementsNum





