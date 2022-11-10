## BG TRIM STEP 2 ##
# Description:
# The function will get BG TRIM on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1

# Constants #
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1']

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
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x0'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.8V as input reference voltage
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 100'
    exec(command)
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 10'
    exec(command)

    # c. Program vref_ldo to take internal BG reference as input
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 0x0'
    exec(command)

    # d. Program vref_ldo resistance divider to take 0.7V as input reference voltage – functional scenario
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg6_inst.vrefldo_vref_range_sel = 10'
    exec(command)
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg32_inst.adc_vrefldo_out_sel = 0x1'
    exec(command)

    # e. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # Take Vref_ldo output as reference voltage for ADC & Supply_buffer which is the case of regular
    # functional mode operation
    command = 'soc_cr_wrapper.' + name + '.inst0.dfvfreg15_inst.adcvrefbufsel = 0x1'
    exec(command)



