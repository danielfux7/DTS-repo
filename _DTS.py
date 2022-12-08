import namednodes as _namednodes
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
ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0' , 'dts_ccf1', 'dts_gt0', 'dts_gt1']
VinADC = 0.77
VrefADC = 0.93
MeasurementsNum = 100

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


def __init__(self):

    while 1:
        print('Choose the DTS for the tests from the list:')
        name = input('dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1 \n')
        print(name)

        if type(name) != str:  # check if string
            print('1')
            continue

        if name in ListDTS:  # check the name is correct
            print('2')
            break

    self.name = name
    self.NumOfDiode = DiodeNum[name]


def method(self):
    print('check')

## BG TRIM STEP 1 ##
# Description:
# The function will get BG TRIM on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
def bg_trim_step1(self):

    print('Starting BG Trim Step 1 on:' + str(self.name))

    # a. program 1.2V LDO reference selection mux to take lvr ref as reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x1'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.93V as input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 6'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 2'
    exec(command)

    # c. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # d. Program ADC external reference mux to select lvr ref
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.adcdfxextvref = 0x0'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg15_inst.adcvrefsel=15'  # need to verify
    exec(command)

    # e. Program vref_ldo output mux to select external reference as adc reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 1'
    exec(command)

    # f. Program ADC supply buffer to select external input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg16_inst.adc_supply_buf_vref_ext_sel = 0x1'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.adc_supply_buf_out_sel = 0x1'
    exec(command)

    # 2. config ADC inputs
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg14_inst.adcvinsel0 = 3'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.anadfxinen = 3'
    exec(command)

    # Select diode RD7 with ovrd and ovrd en (from test plan) not sure its needed TBD
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_en = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_val = 0'
    exec(command)

    # Enable DTS via registers (from test plan)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 1'
    exec(command)

    # 4.For each reading/measurement, take average of few ADC codes, say 100 (to be determined from post
    # silicon observations) to nullify noise (either internal device noise or external noise) impacts
    SumBGRCode = 0
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.adcrawcode'

    for i in range(MeasurementsNum):
        SumBGRCode += eval(command)

    AverageCode = int(SumBGRCode / MeasurementsNum)

    # 5.Save the code into a register. This forms the reference code.
    # Typically, this 10-bit code should be ~848 (0.77/0.93 * 1024)
    # command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgtrimtarget = AverageCode'
    # exec(command)
    self.Step1TrimValue = AverageCode
    print('Step 1 Trim value is: ' + str(self.Step1TrimValue))
    print('finish step1')


## BG TRIM STEP 2 ##
# Description:
# The function will get BG TRIM on of the following strings:
# dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1
def bg_trim_step2(self):
    print('Starting BG Trim Step 2 on:' + str(self.name))

    # a. program 1.2V LDO reference selection mux to take lvr ref as reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.ldo1p2_ext_vref_sel = 0x1'
    exec(command)

    # b. Program 1.2V LDO resistance divider correspondingly to take lvr ref of 0.8V as input reference voltage
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg7_inst.ldo1p2_vref_range_sel = 4'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.ldo1p2_out_sel = 2'
    exec(command)

    # c. Program vref_ldo to take internal BG reference as input
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg4_inst.adc_vrefldo_ext_vref_sel = 0x0'
    exec(command)

    # d. Program vref_ldo resistance divider to take 0.7V as input reference voltage – functional scenario
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg6_inst.vrefldo_vref_range_sel = 2'
    exec(command)
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg32_inst.adc_vrefldo_out_sel = 0x1'
    exec(command)

    # e. Lvr ref_en to be asserted post vccehv is applied & stable
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg5_inst.lvrref_en = 0x1'
    exec(command)

    # Take Vref_ldo output as reference voltage for ADC & Supply_buffer which is the case of regular
    # functional mode operation
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg15_inst.adcvrefbufsel = 0x1'
    exec(command)

    # config ADC - Value must be same as chosen in Step 1 procedure
    command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.dfvfreg14_inst.adcvinsel0 = 3'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.anadfxinen = 3'
    exec(command)

    # Select diode RD7 with ovrd and ovrd en (from test plan) not sure its needed .....
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_en = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.remote_diode_sel_ovr_val = 0'
    exec(command)

    # Disable oneshot mode(from test plan) not sure its needed .....
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0'
    exec(command)

    # 2.Configure ADC to same mode as used in Step 1 (10-bit in this case)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgtrimtarget = self.Step1TrimValue'
    exec(command)

    ## 3-6 Start trimming BG trim bits, took the recipe from test plan

    # Set the BG Trim lower and higher limit codes via register ,the values are not make sense nee to check!! TBD
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimhighlimit = 30'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimlowlimit = 5'
    exec(command)

    # Set the BG Trim start point such that vref_ldo output <0.9V. Update timer to wait for 4.6us for every BG code
    # increment/decrement before starting ADC conversion. This gives enough time for analog to settle.
    ## TBD how to to make sure there is a waiting time between the increment/decrement
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapconfig.bgrtrimrstval = 18'
    exec(command)

    # Enable BG Trim mode
    command = 'cdie.taps.cdie_' + self.name + '.tapconfig.bgtrim_mode = 1'
    exec(command)

    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 1'
    exec(command)

    # Keep polling the BGTRIM Done register till it becomes 1
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrim_done'
    done = 0

    while done == 0:
        done = eval(command)
        done = 1  # just for debug

    # Read the values of BGTRIM FSM state and ensure that BGTRIM is completed without any error
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimfsmstate'
    BGTrimStateFsm = eval(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimerror'
    error = eval(command)

    print(BGTrimStateFsm)

    if error == 1:
        print('calib error')

    SumBGTrimCalib = 0
    command = 'cpu.cdie.taps.cdie_' + self.name + '.tapstatus.bgtrimcode_calib'
    for i in range(MeasurementsNum):
        SumBGTrimCalib += eval(command)

    AverageCode = int(SumBGTrimCalib / MeasurementsNum)
    self.Step2TrimValue = AverageCode
    print('bgtrimcode calib:')
    print(self.Step2TrimValue)

    print('STEP2 finished')


def pretrim_rawcode_readout(self):  # test 5

    print('Starting pre trim rawcode readout :' + str(self.name))

    # Program the BG code obtained from the test "BGR_CALIB_STEP2" into the DTS IP
    command = 'cdie.taps.cdie_' + self.name + '.dtsfusecfg.bgrtrimcode = Step2TrimValue'
    exec(command)

    # Update diode mask to select all the diodes that were calibrated and needed for temperature measurement (RD0 to  RD16)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.active_diode_mask = 0x1'
    exec(command)

    # Disable oneshot mode
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.oneshotmodeen = 0x0'
    exec(command)

    # Enable DTS via registers
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenableovrd = 1'
    exec(command)
    command = 'cpu.cdie.taps.cdie_' + self.name + '.dtsfusecfg.dtsenable = 1'
    exec(command)



def posttrim_temp_readout(self):  # test 6
    pass


def cat_2point_autotrim_check(self):  # test 8
    pass


def postcalib_catblk_trip_check(self):  # test 9
    pass


