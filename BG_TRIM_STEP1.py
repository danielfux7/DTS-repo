## BG TRIM STEP 1 ##
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

    # a. program 1.2V LDO reference selection mux to take lvr ref as reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x1'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.93V as input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 6'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 2'
    exec(command)

    # c. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # d. Program ADC external reference mux to select lvr ref
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.adcdfxextvref = 0x0'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg15_inst.adcvrefsel=15' #need to verify
    exec(command)

    # e. Program vref_ldo output mux to select external reference as adc reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 1'
    exec(command)

    # f. Program ADC supply buffer to select external input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg16_inst.adc_supply_buf_vref_ext_sel = 0x1'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.adc_supply_buf_out_sel = 0x1'
    exec(command)

    # 2. config ADC inputs
    command = 'cpu.cdie.soc_cr_wrapper.' + name + '.inst0.dfvfreg14_inst.adcvinsel0 = 3'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + name + '.tapconfig.anadfxinen = 3'
    exec(command)

    command = ''  # TBD - check wat is the command for getting bgrtirmcode
    SumBGRCode = 0
    # TBD - how to configure to 10 bits code?

    #for i in range(MeasurementsNum):
        #SumBGRCode += eval(command)

    #AverageCode = SumBGRCode / MeasurementsNum  # In what register save the resualt? TBD
    print('finish step1')




