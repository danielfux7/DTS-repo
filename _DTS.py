import namednodes as _namednodes
import pandas as pd
import numpy as np
from config import *
import Asist_Func
from Asist_Func import *
import Diode
from Diode import *


def create_new_path(old_path, tapNum, dtsName):
    parser_path = old_path.split("\\")
    parser_path[len(parser_path) -1] = Taps[int(tapNum)] + '_' + dtsName + '_out.xlsx'
    new_path = parser_path[0] + '\\'
    for i in range(len(parser_path)-2):
        new_path += str(parser_path[i+1]) + '\\'
    new_path += parser_path[len(parser_path)-1]
    print(new_path)
    return new_path

def print_for_fuses():
    print('In order to use this function, make sure to use xlsx/csv files only!')
    print('The files should have 2 columns:')
    print('The default values file contains the columns : "name" and "default_value" ')
    print('The unit values file contains the columns : "name" and "unit_value" ')

def get_number_for_tap():
    tapNum = input('Choose the tap for checking \n 0 - dtsfusecfg \n 1 - tapconfig \n 2 - tapstatus \n ')
    while int(tapNum) > 2:
        print("Wrong Number, try again")
        tapNum = input()
    return tapNum


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
    for i in range(DiodeNum[name]):
        self.diodesList.append(Diode(i))


def method(self):
    print('check')


## BG TRIM STEP 1 ##
def DTS_bg_trim_step1(self):

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
def DTS_bg_trim_step2(self):
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

## Tap Defualt Check ##
def DTS_TAP_Default_Check(self):  # test 1
    dtsName = self.name
    print('In order to use this function, make sure to use xlsx/csv files only!')
    print('The files should have 2 columns:')
    print('The default values file contains the columns : "name" and "default_value" ')
    print('The unit values file contains the columns : "name" and "unit_value" ')
    tapNum = input('Choose the tap for checking \n 0 - dtsfusecfg \n 1 - tapconfig \n 2 - tapstatus \n ')
    while int(tapNum) > 2:
        print("Wrong Number, try again")
        tapNum = input()

    defaultValuePath = input('insert the full path to the defaults values \n') # C:\Users\daniel\default.xlsx
    defaultData = pd.read_excel(defaultValuePath)
    # print('defaultData: ' + str(defaultData))

    defualtNames = list(defaultData.name)
    defualtValues = list(defaultData.default_value)
    defualtDict = {defualtNames[i]: defualtValues[i] for i in range(len(defualtNames))}
    # print('defualtDict: ' + str(defualtDict))

    unitNames = defualtNames
    unitValues = []

    for i in range(len(unitNames)):
        command = 'cpu.cdie.taps.cdie_' + self.name + '.' + Taps[int(tapNum)] + '.' + unitNames[i]
        unitValues.append(eval(command))

    #unitDict = {unitNames[i]: unitValues[i] for i in range(len(defualtNames))}
    #print('unitDict: ' + str(unitDict))

    unitDict = {'name': unitNames ,'unit_value': unitValues}
    unitData = pd.DataFrame.from_dict(unitDict)
    #print('unitDict: ' + str(unitDict))
    print('defaultData:')
    print(defaultData)
    print('unitData:')
    print(unitData)

    finalData = defaultData.merge(unitData, how='left', on='name')
    print('final:')
    print(finalData)

    # define conditions
    conditions = [finalData['default_value'] == finalData['unit_value'],
                  finalData['default_value'] != finalData['unit_value']]

    # define choices
    choices = ['True', 'False']

    # create new column in DataFrame that displays results of comparisons
    finalData['status'] = np.select(conditions, choices, default='Tie')

    exportPath = create_new_path(defaultValuePath,tapNum, dtsName)
    finalData.to_excel(exportPath)

    print(finalData)
    # unitValuePath = input('insert the full path to the unit values \n')
    # #print(unitValuePath)
    # unitData = pd.read_excel(unitValuePath)
    # print(unitData)


## Write Values to Tap Registers ##
# Description: this function will insert values to Tap registers(dtsfusecfg,tapconfig,tapstatus)
def DTS_write_values_func(self):
    print_for_fuses()
    tapNum = get_number_for_tap()
    valuesPath = input('insert the full path to the file with the values  \n')  # C:\Users\daniel\default.xlsx
    data = pd.read_excel(valuesPath)

    dataNames = list(data.name)
    dataValues = list(data.value)

    for i in range(len(dataNames)):
        command = 'cpu.cdie.taps.cdie_' + self.name + '.' + Taps[int(tapNum)] + '.' + unitNames[i] + "=" + unit_value[i]
        exec(command)


## TAP Write Read Check ##
def DTS_TAP_Write_Read_Check(self):  # test 2
    DTS_write_values_func(self)
    DTS_TAP_Default_Check(self)  # the input path will be the as we insert


## CRI Defualt Check ##
def DTS_CRI_Default_Check(self):  # test 3
    pass


## CRI Write Read Check ##
def DTS_CRI_Write_Read_check(self):  # test 4
    pass

## Pre Trim Rawcode Readout ##
def DTS_pretrim_rawcode_readout_particular_temp(self,temp):  # test 5
    #  initialize arrays
    minCodeArr = [0xffff] * self.NumOfDiode
    maxCodeArr = [0] * self.NumOfDiode
    validcodecheck = [True] * self.NumOfDiode
    sumCodeArr = [0] * self.NumOfDiode
    meanCodeArr = [0] * self.NumOfDiode

    print('Starting pre trim rawcode readout : ' + str(self.name))
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self) # Program the BG code obtained from Step 2
    for measNum in range(MeasurementsNum):
        for diode in range(int(self.NumOfDiode)):
            Asist_Func.update_diode_mask(self, int(diode))  # Update diode mask
            Asist_Func.oneshot_disable(self)  # Disable oneshot mode
            Asist_Func.dts_enable(self) # enable DTS via registers

            #if Asist_Func.valid_diode_check(self, diode):  # check if diode exist and valid
            if True:  ####### for debug
                rawCode = Asist_Func.rawcode_read(self, diode)  # read the raw code per some temp and update data
                sumCodeArr[diode] += rawCode
                if minCodeArr[diode] > rawCode:
                    minCodeArr[diode] = rawCode
                if maxCodeArr[diode] < rawCode:
                    maxCodeArr[diode] = rawCode

            else:
                validcodecheck[diode] = False
            Asist_Func.dts_disable(self)  # disable DTS via registers
    print('debug check 1')

    # Do the avg calc and Store the date in the right diode:
    for i in range(self.NumOfDiode):
        # if validcodecheck[i]:
        if True:  ########## for debug:
            meanCodeArr[i] = sumCodeArr[i] / MeasurementsNum
            diodeData = [temp,  meanCodeArr[i], minCodeArr[i], maxCodeArr[i]]
            self.diodesList[i].pretrimData.append(diodeData)
        else:
            meanCodeArr[i] = 'invalid diode'
            self.diodesList[i].valid = False


    print('finish pre trim temp')

## Post Trim Temp Readout ##
def DTS_posttrim_temp_readout(self):  # test 6
    pass

## Cat 2 Points Auto Trim Check ##
def DTS_cat_2point_autotrim_check(self):  # test 8
    pass

## Post Calib Catblk Check ##
def DTS_postcalib_catblk_trip_check(self):  # test 9
    pass


