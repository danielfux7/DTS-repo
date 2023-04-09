import Asist_Func
from Asist_Func import *
import Diode
from Diode import *
import BgwaitPostTrim
from BgwaitPostTrim import *


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


def __init__(self, name):

    while 1:
        # print('Choose the DTS for the tests from the list:')
        # name = input('dts0_aon, dts1, dts2, dts3, dts_ccf0 , dts_ccf1, dts_gt0, dts_gt1 \n')
        print(name)

        if type(name) != str:  # check if string
            print('1')
            continue

        if name == 'dts':
            self.name = name
            return

        if name in ListDTS:  # check the name is correct
            print('2')
            break

    self.name = name
    self.NumOfDiode = DiodeNum[name]
    self.VBE_check_data = {}
    # accuracy data
    self.pre_trim_all_diodes_data = {'dts': [], 'diode': [], 'temperature': [], 'mean_raw_code': [],
                                     'min_raw_code': [], 'max_raw_code': []}
    self.slope_offset_all_diodes_data = {'dts': [], 'diode': [], 'slope': [], 'offset': []}
    self.post_trim_all_diodes_data = {'dts': [], 'OSR_mode': [], 'diode': [], 'temperature': [],
                                      'measured_temperature': [], 'error': []}
    # cattrip data
    self.cat_pre_trim_all_diodes_data = {'dts': [], 'diode': [], 'temperature': [], 'cattrip_code': []}
    self.cat_trim_all_diodes_data = {'dts': [], 'diode': [], 'cat_slope': [], 'cat_offset': [], 'cattrip_code': []}
    self.catblk_post_calib_data = {'dts': [], 'diode': [], 'temperature': [], 'cattrip_temperature': [],
                                   'cat_alert': [], 'status': []}

    # bg wait
    self.bg_wait_code_data = {'dts': [], 'diode': [], 'temperature': [],
                              'mean_raw_code': [], 'mean_raw_code_bg_wait': [],
                              'min_raw_code': [], 'min_raw_code_bg_wait': [],
                              'max_raw_code': [], 'max_raw_code_bg_wait': []}

    # bgref pre post and default check
    self.pre_trim_bg_ref_data = {'dts': [], 'tc': [], 'vtrim_700m': []}
    self.post_trim_bg_ref_data = {'dts': [], 'tc': [], 'vtrim_700m': []}
    self.bg_ref_default_check_data = {'dts': [], 'tc': [], 'vtrim_700m': []}


    # DTD alerts
    self.DTD_NS_alert_direction_0_data = {'dts': [], 'thresh_hold': [], 'temperature_alert_generated': [],
                                          'diff_part_a': [], 'pass_part_a': [], 'temperature_alert_gone': [],
                                          'diff_part_b': [], 'pass_part_b': []}
    self.DTD_NS_alert_direction_1_data = {'dts': [], 'thresh_hold': [], 'temperature_alert_generated': [],
                                          'diff_part_a': [], 'pass_part_a': [], 'temperature_alert_gone': [],
                                          'diff_part_b': [], 'pass_part_b': []}
    self.DTD_sticky_alert_data = {'dts': [], 'thresh_hold_high': [], 'temperature_alert_generated_high': [],
                                  'diff_part_a': [], 'sticky_alert_part_a': [], 'pass_part_a': [],
                                  'thresh_hold_low': [], 'temperature_alert_generated_low': [], 'diff_part_b': [],
                                  'sticky_alert_part_b': [], 'pass_part_b': []}

    self.sleep_delay_check_data = {'DTS_name': [], 'time_expected': [], 'time_measured': [], 'diff_time': [],
                                   'time_expected_dynamic': [], 'time_measured_dynamic': [], 'diff_dyn_time': []}
    self.bg_wait_time_data = {'DTS_name': [], 'time_expected': [], 'time_measured': [], 'diff_time': []}
    self.ADCclkDivData = {25: [], 50: [], 100: []}
    self.adc_clk_all_data = {'DTS_name': [], 'frequency': [], 'temperature': [],
                             'measured_temperature': [], 'error': []}
    self.ana_pwr_seq_data = {'power_gate_enable': [], 'BGR_enable': [], 'LDO1p2V_enabled': [], 'ADC_sup_buf_enable': [],
                             'ADC_sup_buf_enable_delayed': []}
    self.CATBLK_VREF_VBE_VCOMP_data = {'cattrip_code': [], 'comp_vref': [], 'comp_vbe': [],
                                       'vref_min': [], 'vref_max': []}
    self.fusa_check = {'dts': [], 'step_1': [], 'step_2': [], 'step_3': []}
    # for i in range(DiodeNum[name]):
    #     self.diodesList.append(Diode(i))
    self.diodesList = [Diode(i) for i in range(DiodeNum[name])]


def method(self):
    print('check')

## Tap Defualt Check ##
def DTS_TAP_Default_Check(self):  # test 1
    dtsName = self.name
    print('In order to use this function, make sure to use xlsx/csv files only!')
    print('The files should have 2 columns:')
    print('The default values file contains the columns : "name" and "value" ')
    print('The unit values file contains the columns : "name" and "unit_value" ')
    tapNum = input('Choose the tap for checking \n 0 - dtsfusecfg \n 1 - tapconfig \n 2 - tapstatus \n ')
    while int(tapNum) > 2:
        print("Wrong Number, try again")
        tapNum = input()

    if self.name == 'atom_lpc':
        tapNum = 5
    # C:\Users\daniel\fuses_gen1.xlsx
    # C:\Users\daniel\fuses_gen2.xlsx
    defaultValuePath = input('insert the full path to the defaults values \n')  # C:\Users\daniel\default.xlsx
    defaultData = pd.read_excel(defaultValuePath)
    # print('defaultData: ' + str(defaultData))

    defualtNames = list(defaultData.name)
    defualtValues = list(defaultData.value)

    #  Filtering the fields :
    for i in range(len(defualtValues)):
        string = defualtValues[i]
        index = string.find('h')
        defualtValues[i] = int(string[index + 1:], 16)

   # defualtDict = {defualtNames[i]: defualtValues[i] for i in range(len(defualtNames))}
    # print('defualtDict: ' + str(defualtDict))
    defualtDict = {'name': defualtNames, 'default_value': defualtValues}

    unitNames = defualtNames
    unitValues = []

    for i in range(len(unitNames)):
        command = 'cpu.cdie.taps.cdie_' + self.name + '.' + Taps[int(tapNum)] + '.' + unitNames[i]
        #print(unitNames[i])
        unitValues.append(eval(command))


    #unitDict = {unitNames[i]: unitValues[i] for i in range(len(defualtNames))}
    #print('unitDict: ' + str(unitDict))

    unitDict = {'name': unitNames,'unit_value': unitValues}
    unitData = pd.DataFrame.from_dict(unitDict)
    defaultData = pd.DataFrame.from_dict(defualtDict)

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

    exportPath = create_new_path(defaultValuePath, tapNum, dtsName)
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
    if self.name == 'atom_lpc':
        tapNum = 5
    valuesPath = input('insert the full path to the file with the values  \n')  # C:\Users\daniel\default.xlsx
    data = pd.read_excel(valuesPath)

    dataNames = list(data.name)
    dataValues = list(data.value)

    #  Filtering the fields :
    for i in range(len(dataValues)):
        string = dataValues[i]
        index = string.find('h')
        dataValues[i] = int(string[index + 1:], 16)

    for i in range(len(dataNames)):
        command = 'cpu.cdie.taps.cdie_' + self.name + '.' + Taps[int(tapNum)] + '.' + dataNames[i] + "=" \
                  + str(dataValues[i])
        exec(command)


## TAP Write Read Check ##
def DTS_TAP_Write_Read_Check(self):  # test 2
    DTS_write_values_func(self)
    DTS_TAP_Default_Check(self)  # the input path will be the as we insert


## CRI Defualt Check ##
def DTS_CRI_Default_Check(self):  # test 3
    # get the CRI commands
    CRIcommandsPath = input('insert the full path to the CRI file \n')  # C:\Users\daniel\fuses_gen2.xlsx
    CRIData = pd.read_excel(CRIcommandsPath)
    fuseNames = list(CRIData.name)
    CRICommand = list(CRIData.CRICommand)
    CRIValues = list(CRIData.value)
    #CRIValues = [int(x) for x in CRIValues]

    unitValues = []

    #  Filtering the fields :
    for i in range(len(CRIValues)):
        string = CRIValues[i]
        index = string.find('h')
        CRIValues[i] = int(string[index + 1:], 16)

    for i in range(len(fuseNames)):
        command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.' + CRICommand[i]
        unitValues.append(eval(command))



    status = []
    for i in range(len(fuseNames)):
        if unitValues[i] == CRIValues[i]:
            status.append(True)
        else:
            status.append(False)

    data = {'name': fuseNames, 'default_value': CRIValues, 'unit_value': unitValues, 'status': status}
    finalData = pd.DataFrame(data)
    print('final:')
    print(finalData)

    exportPath = create_new_path(CRIcommandsPath, 3, self.name)
    finalData.to_excel(exportPath)

## Write Values to CRI Registers ##
# Description: this function will insert values to CRI registers
def DTS_write_values_to_CRI(self):
    valuesPath = input('insert the full path to the CRI file  \n')  # C:\Users\daniel\fuses_gen2.xlsx
    data = pd.read_excel(valuesPath)

    CRICommand = list(data.CRICommand)
    CRIValues = list(data.value)
    #CRIValues = [int(x) for x in CRIValues]

    #  Filtering the fields :
    for i in range(len(CRIValues)):
        string = CRIValues[i]
        index = string.find('h')
        CRIValues[i] = int(string[index + 1:], 16)


    for i in range(len(CRICommand)):
        command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.' + CRICommand[i] + "=" + str(CRIValues[i])
        exec(command)


## CRI Write Read Check ##
def DTS_CRI_Write_Read_check(self):  # test 4
    DTS_write_values_to_CRI(self)
    DTS_CRI_Default_Check(self)

## Taps VS CRI ##
def taps_against_cri(self):
    valuesPath = input('insert the full path to the CRI file  \n')  # C:\Users\daniel\CRI_commands.xlsx
    data = pd.read_excel(valuesPath)
    fuseNames = list(data.FuseName)
    CRICommand = list(data.CRICommand)

    tapValue = []
    CRIValue = []
    status = []

    for i in range(len(fuseNames)):
        command = 'cpu.cdie.soc_cr_wrapper.' + self.name + '.inst0.' + CRICommand[i]
        CRIValue.append(eval(command))
        command = 'cpu.cdie.taps.cdie_' + self.name + '.' + Taps[0] + '.' + fuseNames[i]
        tapValue.append(eval(command))
        if CRIValue[i] == tapValue[i]:
            status.append(True)
        else:
            status.append(False)

    data = {'name': fuseNames, 'cri_value': CRIValue, 'tap_value': tapValue, 'status': status}
    finalData = pd.DataFrame(data)
    print('final:')
    print(finalData)

    exportPath = create_new_path(valuesPath, 4, self.name)
    finalData.to_excel(exportPath)


## Pre Trim Rawcode Readout ##
def DTS_pretrim_rawcode_readout_particular_temp(self, temp):  # test 5
    #  initialize arrays
    minCodeArr = [0xffff] * self.NumOfDiode
    maxCodeArr = [0] * self.NumOfDiode
    validcodecheck = [True] * self.NumOfDiode
    sumCodeArr = [0] * self.NumOfDiode
    meanCodeArr = [0] * self.NumOfDiode
    pre_trim_titles = ['dts', 'diode', 'temperature', 'mean raw code', 'min raw code', 'max raw code']

    print('Starting pre trim rawcode readout : ' + str(self.name))
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    for measNum in range(MeasurementsNum):
        for diode in range(int(self.NumOfDiode)):
            Asist_Func.update_diode_mask(self, int(diode))  # Update diode mask
            Asist_Func.oneshot_disable(self)  # Disable oneshot mode
            Asist_Func.dts_enable(self)  # enable DTS via registers

            #if Asist_Func.valid_diode_check(self, diode):  # check if diode exist and valid
            if True:  ####### for debug
                rawCode = Asist_Func.rawcode_read(self)  # read the raw code per some temp and update data
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
    for diode in range(self.NumOfDiode):
        # if Asist_Func.valid_diode_check(self, diode):
        if True:  ########## for debug:
            meanCodeArr[diode] = sumCodeArr[diode] / MeasurementsNum
            diodeData = [self.name, diode, temp,  meanCodeArr[diode], minCodeArr[diode], maxCodeArr[diode]]
            self.diodesList[diode].pretrimData.append(diodeData)

            # save data for excel
            self.pre_trim_all_diodes_data['dts'].append(self.name)
            self.pre_trim_all_diodes_data['diode'].append(diode)
            self.pre_trim_all_diodes_data['temperature'].append(temp)
            self.pre_trim_all_diodes_data['mean_raw_code'].append(meanCodeArr[diode])
            self.pre_trim_all_diodes_data['min_raw_code'].append(minCodeArr[diode])
            self.pre_trim_all_diodes_data['max_raw_code'].append(maxCodeArr[diode])

        else:
            meanCodeArr[i] = 'invalid diode'
            self.diodesList[i].valid = False

    print('finish pre trim temp / bgwait code check')


## Trim the diodea ##
def DTS_trim_rawcode(self):
    for diode in range(self.NumOfDiode):
        #if Asist_Func.valid_diode_check(self, diode):
        if self.diodesList[diode].valid:
            temperatures = [item[2] for item in self.diodesList[diode].pretrimData]
            rawcodes = [item[3] for item in self.diodesList[diode].pretrimData]

            rawcodes = [20, 40, 60, 80, 100]   ####################### for debug
            slope, offset = Asist_Func.calculate_slope_and_offset(rawcodes, temperatures)
            print('slope: ' + str(slope))
            print('offset: ' + str(offset))
            Asist_Func.insert_slope_offset_to_diode(self, diode, slope, offset)
            self.slope_offset_all_diodes_data['dts'].append(self.name)
            self.slope_offset_all_diodes_data['diode'].append(diode)
            self.slope_offset_all_diodes_data['slope'].append(slope)
            self.slope_offset_all_diodes_data['offset'].append(offset)


## Post Trim Temp Readout ##
def DTS_posttrim_temp_readout(self, temperature):  # test 6
    Asist_Func.all_dts_disable()  # First disable all the DTS
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    Asist_Func.update_chosen_mask(self, 0xffff)  # update the mask to select all the calibrated dioides
    for i in range(OSRmodesNum):
        avgen = int(i / 4)
        mode = i % 4
        Asist_Func.update_osr_mode(self, avgen, mode)
        Asist_Func.dts_enable(self)  # Enable DTS
        curr = []
        for diode in range(self.NumOfDiode):
            #if Asist_Func.valid_diode_check(self, diode):
            if True: ####################### for debug
                rawcode = Asist_Func.read_temperature_code(self, diode)
                measTemperature = self.diodesList[diode].slope * rawcode_read(self) + self.diodesList[diode].offset
                tempError = temperature - measTemperature
                curr = [self.name, OSRmodes_dict[avgen * 4 + mode], diode,temperature, measTemperature, tempError]
                self.diodesList[diode].posttrimData[OSRmodes[i]].append(curr)

                # collect data for excel
                self.post_trim_all_diodes_data['dts'].append(self.name)
                self.post_trim_all_diodes_data['OSR_mode'].append(OSRmodes_dict[avgen * 4 + mode])
                self.post_trim_all_diodes_data['diode'].append(diode)
                self.post_trim_all_diodes_data['temperature'].append(temperature)
                self.post_trim_all_diodes_data['measured_temperature'].append(measTemperature)
                self.post_trim_all_diodes_data['error'].append(tempError)

        Asist_Func.dts_disable(self)
    Asist_Func.all_dts_disable()
    print('finish one iteration of post trim readout ')


## Cat auto trim Check ##
def DTS_cat_autotrim_check(self, temperature):  # test 7
    #  configuration
    Asist_Func.all_dts_disable()  # First disable all the DTS
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2

    #  check each diode
    for diode in range(self.NumOfDiode):
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, diode)
        Asist_Func.program_digital_viewpin_o_digital_1(self, 0xd)  # I think it should be before the dts enable
        Asist_Func.dts_enable(self)
        Asist_Func.cat_alert_clear(self)
        Asist_Func.reset_cattrip_fsm(self)
        Asist_Func.enable_dts_cattrip_auto_trim_fsm(self)
        Asist_Func.release_cattrip_fsm_reset(self)

        while True:
            fsmCurrState = Asist_Func.read_cattrip_fsm_state(self)
            if fsmCurrState == 3:
                break
            break ############ for debug
        curr = []
        trimcode = Asist_Func.read_cattripcode_out(self, diode)
        curr = [temperature, trimcode]
        self.diodesList[diode].catAutoTrimData.append(curr)
        Asist_Func.dts_disable(self)
    print("finish cat auto trim check")


## Cat 2 Points Auto Trim Check ##
def DTS_cat_2point_autotrim_check(self, temperature):  # test 8
    #  configuration
    Asist_Func.all_dts_disable()  # First disable all the DTS
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2

    for diode in range(self.NumOfDiode):
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, diode)
        Asist_Func.program_digital_viewpin_o_digital_1(self, 0xd)
        Asist_Func.dts_enable(self)
        Asist_Func.cat_alert_clear(self)
        Asist_Func.reset_cattrip_fsm(self)
        Asist_Func.enable_dts_cattrip_auto_trim_fsm(self)
        Asist_Func.release_cattrip_fsm_reset(self)

        while True:
            fsmCurrState = Asist_Func.read_cattrip_fsm_state(self)
            if fsmCurrState == 3:
                break
            break  ############ for debug

        curr = []
        trimcode = Asist_Func.read_cattripcode_out(self, diode)
        curr = [temperature, trimcode]
        self.diodesList[diode].cat2PointsTrimData.append(curr)
        Asist_Func.dts_disable(self)

        # save data for excel
        self.cat_pre_trim_all_diodes_data['dts'].append(self.name)
        self.cat_pre_trim_all_diodes_data['diode'].append(diode)
        self.cat_pre_trim_all_diodes_data['temperature'].append(temperature)
        self.cat_pre_trim_all_diodes_data['cattrip_code'].append(trimcode)

    print('finish 2point cattrip trim')


## Trim cat code for the diodea ##
def DTS_cat_trim_rawcode(self, cattrip_temperature):
    #  calculation of slope and off set
    self.cat_trim_all_diodes_data = {'dts': [], 'diode': [], 'cat_slope': [], 'cat_offset': [], 'cattrip_code': []}
    for diode in range(self.NumOfDiode):
        if self.diodesList[diode].valid:
            if self.gen == 2:
                temperatures = [item[0] for item in self.diodesList[diode].cat2PointsTrimData]
                rawcodes = [item[1] for item in self.diodesList[diode].cat2PointsTrimData]
            else:
                temperatures = [item[0] for item in self.diodesList[diode].catAutoTrimData]
                rawcodes = [item[1] for item in self.diodesList[diode].catAutoTrimData]
            rawcodes = [20, 40, 60, 80, 100]  ####################### for debug
            cat_slope, cat_offset = Asist_Func.calculate_slope_and_offset(rawcodes, temperatures)
            Asist_Func.insert_cat_slope_offset_to_diode(self, diode, cat_slope, cat_offset)
            cattripcode = Asist_Func.convert_temperature_to_rawcode(cattrip_temperature, cat_slope, cat_offset)  # check
            Asist_Func.insert_cattrip_code(self, cattripcode, diode)

            # save data for excel
            self.cat_trim_all_diodes_data['dts'].append(self.name)
            self.cat_trim_all_diodes_data['diode'].append(diode)
            self.cat_trim_all_diodes_data['cat_slope'].append(cat_slope)
            self.cat_trim_all_diodes_data['cat_offset'].append(cat_offset)
            self.cat_trim_all_diodes_data['cattrip_code'].append(cattripcode)
    print('finish cat trim')


## Post Calib Catblk Check ##
def DTS_postcalib_catblk_trim_check(self, temperature_start_point, cattrip_temperature):  # test 9
    Asist_Func.all_dts_disable()  # First disable all the DTS
    if self.gen == 2:
        Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    for diode in range(self.NumOfDiode):
        Asist_Func.update_diode_mask(self, diode)
        catSlope = self.diodesList[diode].catSlope
        catOffset = self.diodesList[diode].catOffset
        cattripcode = Asist_Func.convert_temperature_to_rawcode(cattrip_temperature, catSlope, catOffset)
        Asist_Func.insert_cattrip_code(self, cattripcode, diode)  # program the cattrip trim value
        Asist_Func.program_digital_viewpin_o_digital_1(self, 0xd)
        Asist_Func.dts_enable(self)
        temperature_range = cattrip_temperature - temperature_start_point + 4  # size of shmoo temperatures
        if temperature_range < 0:
            temperature_range = 3
        for curr in range(temperature_range):
            temperature = temperature_start_point + curr
            Asist_Func.temperature_change(temperature)
            if self.gen == 2:
                catAllert = Asist_Func.cattrip_alert(self)  # for gen 2
            else:  # for gen1
                catAllert = Asist_Func.measure_digital_func(self, 0xd)

            if catAllert:
                if temperature < cattrip_temperature:
                    print('alert does not work as expected for temperature: ' + str(temperature))
                    status = False
                else:
                    status = True

            else:  ## no cat siganl
                if temperature >= cattrip_temperature:
                    print('no alert signal for temperature: ' + str(temperature))
                    status = False
                else:
                    status = True

            # add to our data set of diode
            data = [temperature, catAllert, status, cattrip_temperature]
            if cattrip_temperature in self.diodesList[diode].postCalibData:
                self.diodesList[diode].postCalibData[cattrip_temperature].append(data)
            else:
                self.diodesList[diode].postCalibData.update({cattrip_temperature: data})

            # save data for excel
            self.catblk_post_calib_data['dts'].append(self.name)
            self.catblk_post_calib_data['diode'].append(diode)
            self.catblk_post_calib_data['temperature'].append(temperature)
            self.catblk_post_calib_data['cattrip_temperature'].append(cattrip_temperature)
            self.catblk_post_calib_data['cat_alert'].append(catAllert)
            self.catblk_post_calib_data['status'].append(status)
        Asist_Func.dts_disable(self)


## DTS full cattrip calib function  ##
def DTS_full_cattrip_calib_func(self):
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_cat_2point_autotrim_check(self, temperature)
    Asist_Func.temperature_change(25)
    DTS_cat_trim_rawcode(self, 80)
    for cattrip_temperature in cattripTemperatureList:
        start_point_temperature = cattrip_temperature - 10
        Asist_Func.temperature_change(start_point_temperature)
        DTS_postcalib_catblk_trim_check(self, start_point_temperature, cattrip_temperature)
    Asist_Func.temperature_change(25)
    # DTS_cat_trim_rawcode(self, 125)

## BG wait time check ##
def BG_WAIT_TIME_CHECK(self, waitDelay):  # test 11
    Asist_Func.all_dts_disable()
    Asist_Func.update_chosen_mask(self, 3)  # select at least 2 of the connected diodes
    Asist_Func.oneshot_disable(self)
    Asist_Func.program_bg_wait(self,waitDelay)
    Asist_Func.program_digital_viewpin_o_digital_1(self, 0xb)
    print('Measure the time b/w falling edge and rising edge of the signal on o_digital_view[1]')
    print('PASS - The duration b/w the falling an rising edge shall be equal to (waitDelay+1)*10ns')
    while True:
        Asist_Func.dts_enable(self)
        print('measure with the scope')
        repeat = input('press y for repeat the measurement, press n to continue the test \n')
        if repeat == 'n':
            break
        Asist_Func.dts_disable(self)
    num = input('Enter the time you measured through the scope \n')
    time_measured = float(num)
    time_expected = (waitDelay + 1) * 10e-9
    diff_time = abs(time_expected - time_measured)
    self.bg_wait_time_data['DTS_name'].append(self.name)
    self.bg_wait_time_data['time_expected'].append(time_expected)
    self.bg_wait_time_data['time_measured'].append(time_measured)
    self.bg_wait_time_data['diff_time'].append(diff_time)


## BG wait code check ##
def BG_WAIT_CODE_CHECK(self, temperature, bgWait):  # test 12
    print('do this test after pre trim  ')
    DTS_pretrim_rawcode_readout_particular_temp(self, temperature, bgWait)


## sleep delay check ##
def SLEEP_DELAY_CHECK(self, sleepTime, sleepTimeDynamic):  # sleepTimeDynamic != so it will be the dynamic test
    Asist_Func.all_dts_disable()
    Asist_Func.update_chosen_mask(self, 0)
    Asist_Func.program_sleep_timer(self, sleepTime)
    Asist_Func.program_digital_viewpin_o_digital_1(self, 0xc)
    print('Measure the time b/w falling edge and rising edge of the signal on o_digital_view[1] on scope')
    print('PASS - The duration b/w the falling an rising edge shall be equal to (sleepTime*2^12+1000)*10ns')
    input('press any key to measure with the scope the dts: ' + self.name) + '\n'
    while True:
        Asist_Func.dts_enable(self)
        repeat = input('press y for repeat the measurement, press n to continue the test \n')
        if repeat == 'n':
            break
        Asist_Func.dts_disable(self)
    num = input('Enter the time you measured on the dts: ' + self.name +
                ' through the scope \n For dynamic test: after inserting the time be ready to '
                'capture the next measurement \n ')
    time_measured = float(num)
    time_expected = (sleepTime * pow(2, 12) + 1000) * 10e-9
    diff_time = abs(time_expected - time_measured)
    self.sleep_delay_check_data['DTS_name'].append(self.name)
    self.sleep_delay_check_data['time_expected'].append(time_expected)
    self.sleep_delay_check_data['time_measured'].append(time_measured)
    self.sleep_delay_check_data['diff_time'].append(diff_time)
    if sleepTimeDynamic:
        Asist_Func.program_sleep_timer(self, sleepTimeDynamic)
        while True:
            Asist_Func.enable_dynamic_update(self)
            print('measure with the scope')
            repeat = input('press y for repeat the measurement, press n to continue the test \n')
            if repeat == 'n':
                break
            Asist_Func.disable_dynamic_update(self)
        num = input('Enter the time you measured through the scope for dynamic enable \n')
        time_measured_dynamic = float(num)
        time_expected_dynamic = (sleepTimeDynamic * pow(2, 12) + 1000) * 10e-9
        diff_dyn_time = abs(time_expected_dynamic - time_measured_dynamic)
        self.sleep_delay_check_data['time_expected_dynamic'].append(time_expected_dynamic)
        self.sleep_delay_check_data['time_measured_dynamic'].append(time_measured_dynamic)
        self.sleep_delay_check_data['diff_dyn_time'].append(diff_dyn_time)
    else:  # in order to have same lengths of arrays
        self.sleep_delay_check_data['time_expected_dynamic'].append('not_dynamic')
        self.sleep_delay_check_data['time_measured_dynamic'].append('not_dynamic')
        self.sleep_delay_check_data['diff_dyn_time'].append('not_dynamic')



## dynamic sleep delay check ##
def DYNAMIC_SLEEP_DELAY_CHECK(self, sleepTime):
    print('before this test do the test: SLEEP_DELAY_CHECK')
    Asist_Func.program_sleep_timer(self, sleepTime)
    Asist_Func.enable_dynamic_update(self)
    print('Measure the time b/w falling edge and rising edge of the signal on o_digital_view[1]')
    print('PASS - The duration b/w the falling an rising edge shall be equal to (sleepTime*2^12+1000)*10ns')


## adc clock div test ##
def ADC_CLK_DIV_TEST(self, temperature, diode):  # test 14
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    for freq in FrequenciesList:
        Asist_Func.update_chosen_mask(self, diode)
        Asist_Func.program_adc_clock_freq(self, FrequenciesDict[freq])
        Asist_Func.dts_enable(self)
       # if Asist_Func.valid_diode_check(self, diode):  # check some diode you choose
        if True:   ########################################## for debug
            measTemperature = Asist_Func.read_temperature_code(self, diode)
            tempError = temperature - measTemperature
            curr = [temperature, measTemperature, tempError]
            self.ADCclkDivData[freq].append(curr)
            # save data for excel
            self.adc_clk_all_data['DTS_name'].append(self.name)
            self.adc_clk_all_data['frequency'].append(freq)
            self.adc_clk_all_data['temperature'].append(temperature)
            self.adc_clk_all_data['measured_temperature'].append(measTemperature)
            self.adc_clk_all_data['error'].append(tempError)
        else:
            print('invalid diode')
        Asist_Func.dts_disable(self)


## AON_OVRD_DTS_FUNC_CHECK ##
def AON_OVRD_DTS_FUNC_CHECK(self):
    Asist_Func.dts_disable(self)
    Asist_Func.aon_enable(self)
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_posttrim_temp_readout(self, temperature)
    Asist_Func.aon_disable(self)


def get_to_high_temperature_limit_direction_1(self, minTemperature, maxTemperature, threshold):
    Asist_Func.temperature_change(minTemperature)
    curr = 0
    while maxTemperature > Asist_Func.read_temperature_code(self, 0):
        print('increasing the temperature by 1 degree')
        Asist_Func.temperature_change(minTemperature + curr)
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if Asist_Func.dtd_ns_alert(self):
            self.DTD_NS_alert_direction_1_data['temperature_alert_generated'].append(currTemp)
            self.DTD_NS_alert_direction_1_data['diff_part_a'].append(currTemp - threshold)  # might be also negative
            if currTemp < threshold:
                print('There is an alert before we crossed the threshold temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_1_data['pass_part_a'].append(0)  # no pass part a
                break
            else:
                print('NS alerted when temp crossed the threshhold as expected for the temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_1_data['pass_part_a'].append(1)  # pass part a , need to check what spec?
                break
        curr += 1
    Asist_Func.temperature_change(maxTemperature)  # preparing for part b of the test


def get_to_low_temperature_limit_direction_1(self, minTemperature, maxTemperature, threshold):
    Asist_Func.temperature_change(maxTemperature)
    curr = 0
    while minTemperature < Asist_Func.read_temperature_code(self, 0):
        print('decreasing the temperature by 1 degree')
        Asist_Func.temperature_change(minTemperature - curr)
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if not Asist_Func.dtd_ns_alert(self):
            self.DTD_NS_alert_direction_1_data['temperature_alert_gone'].append(currTemp)
            self.DTD_NS_alert_direction_1_data['diff_part_b'].append(currTemp - threshold)  # can be also negative
            if currTemp >= threshold:
                print('There is not an alert before we crossed back the threshold temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_1_data['pass_part_b'].append(0)  # no pass part b
                break
            else:
                print('NS alert gone when temp crossed the TH as expected for the temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_1_data['pass_part_b'].append(1)  # pass part b, need to check what spec?
                break
        curr += 1
    Asist_Func.temperature_change(minTemperature)


def get_to_high_temperature_limit_direction_0(self, minTemperature,maxTemperature, threshold):
    Asist_Func.temperature_change(minTemperature)
    curr = 0
    while maxTemperature > Asist_Func.read_temperature_code(self, 0):
        print('increasing the temperature by 1 degree')
        Asist_Func.temperature_change(minTemperature + curr)
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if not Asist_Func.dtd_ns_alert(self):
            self.DTD_NS_alert_direction_0_data['temperature_alert_gone'].append(currTemp)
            self.DTD_NS_alert_direction_0_data['diff_part_b'].append(currTemp - threshold)  # can be also negative
            if currTemp <= threshold:
                print('There is no alert before crossed back the threshold temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_0_data['pass_part_b'].append(0)  # no pass part a
                break
            else:
                print('NS alert gone when temp crossed the TH as expected for the temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_0_data['pass_part_b'].append(1)  # pass part a , need to check what spec?
                break
        curr += 1
    Asist_Func.temperature_change(maxTemperature)


def get_to_low_temperature_limit_direction_0(self, minTemperature, maxTemperature,threshold):
    Asist_Func.temperature_change(maxTemperature)
    curr = 0
    while minTemperature < Asist_Func.read_temperature_code(self, 0):
        print('decreasing the temperature by 1 degree')
        Asist_Func.temperature_change(maxTemperature - curr)
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if Asist_Func.dtd_ns_alert(self):
            self.DTD_NS_alert_direction_0_data['temperature_alert_generated'].append(currTemp)
            self.DTD_NS_alert_direction_0_data['diff_part_a'].append(currTemp - threshold)  # can be also negativ
            if currTemp > threshold:
                print('There is an alert before we crossed the threshold temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_0_data['pass_part_a'].append(0)  # no pass part a
                break
            else:
                print('NS alerted when temp crossed the threshhold as expected for the temperature: ' + str(currTemp))
                self.DTD_NS_alert_direction_0_data['pass_part_a'].append(1)  # pass part a , need to check what spec?
                break
        curr += 1
    Asist_Func.temperature_change(minTemperature)  # preparing for part b of the test


## DTD non sticky alert test ## test 16
def DTD_NS_ALERT_TEST_before_update(self, maxTemperature, minTemperature, threshold, direction):
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    for diode in range(self.NumOfDiode):
        Asist_Func.update_diode_mask(self, diode)
        Asist_Func.reinsert_calculated_existed_slope_offset(self, diode)
        Asist_Func.dts_enable(self)
        Asist_Func.dtd_ns_alert_threshold_direction_insert(self, threshold, direction)
        if direction:
            if Asist_Func.valid_diode_check(self, diode):
                pass_flag = 0
                get_to_high_temperature_limit_direction_1(self, diode, maxTemperature, threshold, pass_flag)
                if not Asist_Func.dtd_ns_alert(self):
                    self.diodesList[diode].PassNsAlertTest = 0
                    print('There is no alert after crossing the threshold temperature')
                    print('Lower the temperature to the minimum temperature value')
                    while minTemperature < Asist_Func.read_temperature_code(self, diode):
                        input('Decrease the temperature to the minimum value and press any key to continue')
                        currTemp = Asist_Func.read_temperature_code(self, diode)
                        print('the current temperature for the diode ' + str(diode) + ' is:')
                        print(currTemp)
                    continue  # check the next diode

                else:  # part 2 of the test is lower the temeerature to the min value and check if alert is gone
                    pass_flag = 0
                    get_to_low_temperature_limit_direction_1(self, diode, minTemperature, threshold, pass_flag)
                    if Asist_Func.dtd_ns_alert(self):
                        print('There is alert after crossing the threshold temperature')
                        self.diodesList[diode].PassNsAlertTest = 0

            else:
                print('diode not valid')

        else:  # direction is 0, now we will check the the other direction, triggered when below threshold
            if Asist_Func.valid_diode_check(self, diode):
                pass_flag = 0
                get_to_low_temperature_limit_direction_0(self, diode, minTemperature, threshold, direction )
                if not Asist_Func.dtd_ns_alert(self):
                    self.diodesList[diode].PassNsAlertTest = 0
                    print('There is no alert after crossing the threshold temperature')
                    print('Increase the temperature to the max temperature value')
                    while maxTemperature > Asist_Func.read_temperature_code(self, diode):
                        input('Decrease the temperature to the max value and press any key to continue')
                        currTemp = Asist_Func.read_temperature_code(self, diode)
                        print('the current temperature for the diode ' + str(diode) + ' is:')
                        print(currTemp)
                    continue  # check the next diode

                else:  # part 2 of the test is lower the temeerature to the min value and check if alert is gone
                    pass_flag = 0
                    get_to_high_temperature_limit_direction_0(self, diode, minTemperature, threshold, pass_flag)
                    if Asist_Func.dtd_ns_alert(self):
                        print('There is alert after crossing the threshold temperature')
                        self.diodesList[diode].PassNsAlertTest = 0

            else:
                print('diode not valid')


## DTD non sticky alert test ## test 16
def DTD_NS_ALERT_TEST(self, maxTemperature, minTemperature, threshold, direction):
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    Asist_Func.update_diode_mask(self, 0)
    Asist_Func.reinsert_calculated_existed_slope_offset(self, 0)
    Asist_Func.dts_enable(self)
    Asist_Func.dtd_ns_alert_threshold_direction_insert(self, threshold, direction)
    self.DTD_NS_alert_direction_1_data['dts'].append(self.name)
    self.DTD_NS_alert_direction_0_data['dts'].append(self.name)
    self.DTD_NS_alert_direction_1_data['thresh_hold'].append(threshold)
    self.DTD_NS_alert_direction_0_data['thresh_hold'].append(threshold)
    if direction:
        #if Asist_Func.valid_diode_check(self, 0):  # the diode num can be modified
        if True: ######################### for debug
            get_to_high_temperature_limit_direction_1(self, minTemperature,maxTemperature, threshold)
            if not Asist_Func.dtd_ns_alert(self):
                print('There is no alert after crossing the threshold temperature')
                print('Therefore, part b of this test can not be done ')
                self.DTD_NS_alert_direction_1_data['temperature_alert_generated'].append('not valid')
                self.DTD_NS_alert_direction_1_data['diff_part_a'].append('not valid')
                self.DTD_NS_alert_direction_1_data['pass_part_a'].append(0)
                self.DTD_NS_alert_direction_1_data['temperature_alert_gone'].append('not valid')
                self.DTD_NS_alert_direction_1_data['diff_part_b'].append('not valid')
                self.DTD_NS_alert_direction_1_data['pass_part_b'].append('not valid')

            else:  # part b of the test is lower the temeerature to the min value and check if alert is gone
                get_to_low_temperature_limit_direction_1(self, minTemperature, maxTemperature, threshold)
                if Asist_Func.dtd_ns_alert(self):
                    print('There is alert after crossing back the threshold temperature')
                    self.DTD_NS_alert_direction_1_data['temperature_alert_gone'].append('not valid')
                    self.DTD_NS_alert_direction_1_data['diff_part_b'].append('not valid')
                    self.DTD_NS_alert_direction_1_data['pass_part_b'].append(0)

        else:
            print('diode not valid')

    else:  # direction is 0, now we will check the the other direction, triggered when below threshold
        #if Asist_Func.valid_diode_check(self, 0):
        if True: ################################ for debug
            get_to_low_temperature_limit_direction_0(self, maxTemperature, minTemperature, threshold)
            if not Asist_Func.dtd_ns_alert(self):
                print('There is no alert after crossing the threshold temperature')
                print('Increase the temperature to the max temperature value')
                self.DTD_NS_alert_direction_0_data['temperature_alert_generated'].append('not valid')
                self.DTD_NS_alert_direction_0_data['diff_part_a'].append('not valid')
                self.DTD_NS_alert_direction_0_data['pass_part_a'].append(0)
                self.DTD_NS_alert_direction_0_data['temperature_alert_gone'].append('not valid')
                self.DTD_NS_alert_direction_0_data['diff_part_b'].append('not valid')
                self.DTD_NS_alert_direction_0_data['pass_part_b'].append('not valid')

            else:  # part 2 of the test is lower the temeerature to the min value and check if alert is gone
                get_to_high_temperature_limit_direction_0(self, maxTemperature, minTemperature, threshold)
                if Asist_Func.dtd_ns_alert(self):
                    print('There is alert after crossing the threshold temperature')
                    self.DTD_NS_alert_direction_0_data['temperature_alert_gone'].append('not valid')
                    self.DTD_NS_alert_direction_0_data['diff_part_b'].append('not valid')
                    self.DTD_NS_alert_direction_0_data['pass_part_b'].append(0)

        else:
            print('diode not valid')

    print('direction = 1 :')
    print(self.DTD_NS_alert_direction_1_data)
    print('direction = 0 :')
    print(self.DTD_NS_alert_direction_0_data)


def get_to_high_and_low_sticky_temperature_limit(self, maxTemperature, minTemperature, highThreshold,lowThreshold):
    curr = 0
    alert_flag = 0
    middle_temperature = (highThreshold - lowThreshold) / 2 + lowThreshold
    Asist_Func.temperature_change(middle_temperature)
    self.DTD_sticky_alert_data['dts'].append(self.name)
    self.DTD_sticky_alert_data['thresh_hold_high'].append(highThreshold)
    self.DTD_sticky_alert_data['thresh_hold_low'].append(lowThreshold)
    while maxTemperature > Asist_Func.read_temperature_code(self, 0):
        print('Increasing the temperature by step of one degree')
        Asist_Func.temperature_change(middle_temperature + curr)
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if Asist_Func.dtd_alert(self):
            alert_flag = 1
            self.DTD_sticky_alert_data['temperature_alert_generated_high'].append(currTemp)
            self.DTD_sticky_alert_data['diff_part_a'].append(currTemp - highThreshold)
            if currTemp < highThreshold:
                print('There is an alert before we crossed the threshold temperature: ' + str(currTemp))
                self.DTD_sticky_alert_data['pass_part_a'].append(0)  # no pass
            else:
                print('Sticky alert alerted as expected for the temperature: ' + str(currTemp))
                self.DTD_sticky_alert_data['pass_part_a'].append(1)

        if alert_flag:  # sticky alert check before and after sticky clear
            Asist_Func.temperature_change(middle_temperature)
            if Asist_Func.dtd_alert(self):  # pass - if still high
                Asist_Func.clear_sticky_alert(self)
                if not Asist_Func.dtd_alert(self):  # pass - if the sticky alert cleared
                    self.DTD_sticky_alert_data['sticky_alert_part_a'].append('pass')
                    break

            #  sticky alert fail
            len_arr = len(self.DTD_sticky_alert_data['pass_part_a'])
            self.DTD_sticky_alert_data['pass_part_a'][len_arr - 1] = 0
            self.DTD_sticky_alert_data['sticky_alert_part_a'].append('no pass')
            self.DTD_sticky_alert_data['temperature_alert_generated_low'].append('not valid')
            self.DTD_sticky_alert_data['diff_part_b'].append('not valid')
            self.DTD_sticky_alert_data['pass_part_b'].append('not valid')  # cant continue when cant clear alert
            self.DTD_sticky_alert_data['sticky_alert_part_b'].append('not valid')
            return
        curr += 1

    if not alert_flag:
        print('No sticky alert although the temperature is above the high limit')
        self.DTD_sticky_alert_data['temperature_alert_generated_high'].append('not valid')
        self.DTD_sticky_alert_data['diff_part_a'].append('not valid')
        self.DTD_sticky_alert_data['pass_part_a'].append(0)
        self.DTD_sticky_alert_data['sticky_alert_part_a'].append('not valid')

    # Starting par b :
    curr = 0
    alert_flag = 0
    print('Get the temperature between the limits')
    Asist_Func.temperature_change(middle_temperature)
    Asist_Func.clear_sticky_alert(self)
    while minTemperature < Asist_Func.read_temperature_code(self, 0):
        print('Decreasing the temperature by one degree')
        currTemp = Asist_Func.read_temperature_code(self, 0)
        print('the current temperature for the diode ' + str(0) + ' is:')
        print(currTemp)
        if Asist_Func.dtd_alert(self):
            alert_flag = 1
            self.DTD_sticky_alert_data['temperature_alert_generated_low'].append(currTemp)
            self.DTD_sticky_alert_data['diff_part_b'].append(lowThreshold - currTemp)
            if currTemp > lowThreshold:
                print('There is an alert before we crossed the threshold temperature: ' + str(currTemp))
                self.DTD_sticky_alert_data['pass_part_b'].append(0)  # no pass
            else:
                print('Sticky alert alerted as expected for the temperature: ' + str(currTemp))
                self.DTD_sticky_alert_data['pass_part_b'].append(1)

        # check sticky alert
        if alert_flag:  # sticky alert check before and after sticky clear
            Asist_Func.temperature_change(middle_temperature)
            if Asist_Func.dtd_alert(self):  # pass - if still high
                Asist_Func.clear_sticky_alert(self)
                if not Asist_Func.dtd_alert(self):  # pass - if the sticky alert cleared
                    self.DTD_sticky_alert_data['sticky_alert_part_b'].append('pass')
                    break

            #  sticky alert fail
            len_arr = len(self.DTD_sticky_alert_data['pass_part_b'])
            self.DTD_sticky_alert_data['pass_part_b'][len_arr - 1] = 0
            self.DTD_sticky_alert_data['sticky_alert_part_b'].append('no pass')
            return
        curr += 1

    if not alert_flag:
        print('No sticky alert although the temperature is above the high limit')
        self.DTD_sticky_alert_data['temperature_alert_generated_low'].append('not valid')
        self.DTD_sticky_alert_data['diff_part_b'].append('not valid')
        self.DTD_sticky_alert_data['pass_part_b'].append(0)
        self.DTD_sticky_alert_data['sticky_alert_part_b'].append('not valid')


## DTD sticky alert test ## test 17
def DTD_STICKY_ALERT_TEST(self, maxTemperature, minTemperature, lowLimit, highLimit):
    print('Make sure the current temperature is between the limits ')
    Asist_Func.all_dts_disable()
    Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
    Asist_Func.update_diode_mask(self, 0)
    Asist_Func.reinsert_calculated_existed_slope_offset(self, 0)
    Asist_Func.dts_enable(self)
    Asist_Func.dtd_sticky_thr_high(self, highLimit)
    Asist_Func.dtd_sticky_thr_low(self, lowLimit)
    #if Asist_Func.valid_diode_check(self, 0):
    if True: ############################# for debug
        get_to_high_and_low_sticky_temperature_limit(self, maxTemperature, minTemperature, highLimit,lowLimit)
    else:
        print('diode not valid')
    Asist_Func.dts_disable(self)


## bgcore vbg vtrim 700m ## for test 19, 20
def BGCORE_VBG_vtrim(self, bgtrimcode, tc):
    vtrim_700m_dict = {'dts': [], 'tc': [], 'vtrim_700m': []}
    vtrim_700m_dict['dts'].append(self.name)
    vtrim_700m_dict['tc'].append(tc)
    Asist_Func.all_dts_disable()
    Asist_Func.set_any_bg_trim_code(self, bgtrimcode)
    if tc != -1:
        Asist_Func.set_any_tc(self, tc)
    Asist_Func.program_viewanasigsel(self, int('0b11001111', 2))
    Asist_Func.dts_enable(self)
    print('Measure the vtrim_700m voltage through the analog DFT via bump xx_b_dts_anaview_0_dts_lv and press any key')
    vtrim_700m = Asist_Func.measure_analog_func(self, 0)
    vtrim_700m_dict['vtrim_700m'].append(vtrim_700m)
    Asist_Func.dts_disable(self)
    return vtrim_700m_dict


## DTS pre trim bg ref check ## test 19
def DTS_DEFAULT_BGREF_CHECK(self):
    temp_dict = BGCORE_VBG_vtrim(self, int('0b10000', 2), 3)
    self.bg_ref_default_check_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.bg_ref_default_check_data,
                                                                                      temp_dict)


## DTS pre trim bg ref check ## test 20
def DTS_PRETRIM_BGREF_CHECK(self):
    tc = Asist_Func.get_curr_tc(self)
    temp_dict = BGCORE_VBG_vtrim(self, 0, tc)
    self.pre_trim_bg_ref_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.pre_trim_bg_ref_data, temp_dict)
    temp_dict = BGCORE_VBG_vtrim(self, int('0b11001', 2), tc)
    self.pre_trim_bg_ref_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.pre_trim_bg_ref_data, temp_dict)
    temp_dict = BGCORE_VBG_vtrim(self, int('0b11111', 2), tc)
    self.pre_trim_bg_ref_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.pre_trim_bg_ref_data, temp_dict)


def DTS_POSTTRIM_BGREF_CHECK(self):
    bgtrimcode = self.Step2TrimValue
    for tc in range(8):
        temp_dict = BGCORE_VBG_vtrim(self, bgtrimcode, tc)
        self.post_trim_bg_ref_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.post_trim_bg_ref_data,
                                                                                      temp_dict)


## ana pwr seq view ##
def ANA_PWR_SEQ_VIEW(self):  # test 24
    Asist_Func.all_dts_disable()
    Asist_Func.program_digital_viewpin_o_digital_0(self, 0xe)
    for digital_signal in anaPwrSeqSignalList:
        Asist_Func.dts_disable(self)
        Asist_Func.program_digital_viewpin_o_digital_1(self, anaPwrSeqSignalDict[digital_signal])
        Asist_Func.dts_enable(self)
        print('Measure the time b/w falling edge viewpin0 and each of the signal on Viewpin1 '
              'by running multiple iterations of this test.')
        print('use scope and get out the 2 digital signal and trigger the falling of DTS enable')
        while True:
            input('press any key to disable the DTS')
            Asist_Func.dts_disable(self)
            num = input('insert the time between the dts disable to the falling of the measured signal \n')
            time_passed = float(num)
            self.ana_pwr_seq_data[digital_signal].append(time_passed)
            Asist_Func.dts_enable(self)
            repeat = input('press y to repeat the measurement or n to go to the next signal \n')
            if repeat == 'n':
                break


def default_setup_configuration(self):  # as the default values
    Asist_Func.dts_disable(self)
    Asist_Func.ldo1p2_ext_vref_select(self, 1)  # Program 1.2VLDO reference selection mux to take lvrref as ref voltage
    Asist_Func.ldo1p2_vref_range_select(self, 4)
    Asist_Func.ldo1p2_out_sel(self, 2)
    Asist_Func.adc_vrefldo_ext_vref_sel(self, 0)
    Asist_Func.vrefldo_vref_range_sel(self, 2)
    Asist_Func.adc_vrefldo_out_sel(self, 1)
    Asist_Func.lvrrref_dis(self)  # not really need, because we don't have external voltage, but also harmless
    Asist_Func.adc_vref_buf_select(self, 1)  # buf enable - functional mode

    # Program supply_ldo to functional mode
    Asist_Func.adc_supply_buf_vref_ext_select(self, 0)
    Asist_Func.adc_supply_buf_out_select(self, 2)

    # Apply Vbe as input to AZ buffer through DFC input
    Asist_Func.adcvinsel0_select(self, 0)

    # Program ADC reference mux to select Vbgr
    Asist_Func.adcdfxextvref_select(self, 0)
    Asist_Func.adc_vref_select(self, 0)

    Asist_Func.dts_enable(self)


def bgr_calib_step1_configuration(self): #######add fusa enabe to step 1 and 2
    Asist_Func.ldo1p2_ext_vref_select(self, 1)  # Program 1.2VLDO reference selection mux to take lvrref as ref voltage
    Asist_Func.ldo1p2_vref_range_select(self, 6)  ############# need to be modfied to 100
    Asist_Func.ldo1p2_out_sel(self, 2)  # Program 1.2VLDO resistance divider to take lvrref of 0.93V as input ref vol
    Asist_Func.lvrrref_en(self)  # Enable for external reference
    Asist_Func.adcdfxextvref_select(self, 0)
    Asist_Func.adc_vref_select(self, 15)  # Program ADC external reference mux to select lvrref
    Asist_Func.adc_vrefldo_ext_vref_sel(self, 1)  #
    Asist_Func.adc_supply_buf_vref_ext_select(self, 0)  ############### need to be 1 check it
    Asist_Func.adc_supply_buf_out_select(self, 2)  # Program ADC supply buffer to select external input reference volt

    # apply external voltage
    Asist_Func.apply_voltage_i_ana_dfx_1(VinADC, 0)
    Asist_Func.adcvinsel0_select(self, 3)
    Asist_Func.anadfxinen_select(self, 3)

    # Select diode RD7 with ovrd and ovrd en
    Asist_Func.diode_sel_ovr_en(self)
    Asist_Func.diode_sel_ovr_val(self, 0)

    # Program supply_ldo to take external refrence as input
    Asist_Func.adc_supply_buf_vref_ext_select(self, 1)
    Asist_Func.adc_supply_buf_out_select(self, 1)


def bgr_calib_step2_configuration(self):
    Asist_Func.ldo1p2_ext_vref_select(self, 1)  # Program 1.2VLDO reference selection mux to take lvrref as ref voltage
    Asist_Func.ldo1p2_vref_range_select(self, 4)
    Asist_Func.ldo1p2_out_sel(self, 2) # Program 1.2VLDO resistance divider to take lvrref of 0.8V as input ref vol
    Asist_Func.adc_vrefldo_ext_vref_sel(self, 0)  # Program vref_ldo to take internal BG reference as input
    Asist_Func.vrefldo_vref_range_sel(self, 2)
    Asist_Func.adc_vrefldo_out_sel(self, 1)  # Program vrefldo resistance divider take 0.7V as input ref vol-functional
    Asist_Func.lvrrref_en(self)  # Enable for external reference
    Asist_Func.adc_vref_buf_select(self, 1)  # buf enable - functional mode

    # apply external voltage
    Asist_Func.apply_voltage_i_ana_dfx_1(VinADC, 0)
    Asist_Func.adcvinsel0_select(self, 3)
    Asist_Func.anadfxinen_select(self, 3)

    # Select diode RD7 with ovrd and ovrd en
    Asist_Func.diode_sel_ovr_en(self)
    Asist_Func.diode_sel_ovr_val(self, 0)

    # Program supply_ldo to functional mode
    Asist_Func.adc_supply_buf_vref_ext_select(self, 0)
    Asist_Func.adc_supply_buf_out_select(self, 2)


## BG TRIM STEP 1 ##
def DTS_bg_trim_step1(self):
    print('Starting BG Trim Step 1 on:' + str(self.name))
    Asist_Func.dts_disable(self)
    bgr_calib_step1_configuration(self)
    Asist_Func.dts_enable(self)
    sumBGRCode = 0
    for i in range(MeasurementsNum):
        sumBGRCode += Asist_Func.rawcode_read(self)

    averageCode = int(sumBGRCode / MeasurementsNum)
    self.Step1TrimValue = averageCode
    print('Step 1 Trim value is: ' + str(self.Step1TrimValue))
    print('finish step1')


## BG TRIM STEP 2 ##
def DTS_bg_trim_step2(self):
    print('Starting BG Trim Step 2 on:' + str(self.name))
    Asist_Func.dts_disable(self)
    bgr_calib_step2_configuration(self)
    Asist_Func.oneshot_enable(self)
    Asist_Func.bgtrimtarget(self, self.Step1TrimValue)
    Asist_Func.bgrtrimhighlimit(self, 30)
    Asist_Func.bgrtrimlowlimit(self, 5)
    Asist_Func.bgrtrimrstval(self, 18)
    Asist_Func.bgtrim_mode_enable(self)
    Asist_Func.dts_enable(self)

    while True:  # Keep polling the BGTRIM Done register till it becomes 1
        if Asist_Func.bgtrim_done(self):
            break
        break ######### debug

    bg_fsm_state = Asist_Func.bgtrim_fsm_state(self)
    bg_trim_error = Asist_Func.bgtrim_error(self)
    if bg_fsm_state == 4 and bg_trim_error == 0:
        print('PASS')
        sumBGRCode = 0
        for i in range(MeasurementsNum):
            sumBGRCode += Asist_Func.bgtrimcode_calib(self)

        averageCode = int(sumBGRCode / MeasurementsNum)
        self.Step2TrimValue = averageCode
        Asist_Func.program_bg_code(self)
        print('Step 2 Trim value is: ' + str(self.Step2TrimValue))
        print('finish step2')
    else:
        print('BGR calibration error')


## VBE check ##
def DTS_RD_VBE_Check(self, temperature):
    # configuration
    Asist_Func.temperature_change(temperature)
    Asist_Func.all_dts_disable()
    if self.gen == 2:
        Asist_Func.program_bg_code(self)  # Program the BG code obtained from Step 2
        Asist_Func.program_viewanasigsel(self, 0b11001001)  # VBE1
        default_setup_configuration(self)
    else:
        Asist_Func.program_viewanasigsel(self, 6)  # Select the analog dft mux to out the RD VBE gen1

    # initialize
    dts_name = []
    temperatures = []
    diode_num = []
    voltage_measured = []
    rawcode = []
    rawcode_calculation = []
    error = []

    for diode in range(self.NumOfDiode):
        Asist_Func.dts_disable(self)
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, diode)
        Asist_Func.dts_enable(self)
        #if Asist_Func.valid_diode_check(self, diode):
        if True:  ###### for debug!!!!!
            dts_name.append(self.name)
            temperatures.append(temperature)
            diode_num.append(diode)
            rawcode.append(Asist_Func.rawcode_read(self))
            voltage_measured.append(Asist_Func.measure_analog_func(self,  0b11001001))
            calculation = (voltage_measured[diode] / VrefADC) * primaryCounter
            rawcode_calculation.append(calculation)
            gap = rawcode[diode] - calculation
            error.append(gap)
            if temperature == 100 and diode == 0:
                self.vbe_diode0_100_deg = voltage_measured[diode]

    # Add data to the DTS class
    if self.gen == 2:
        self.VBE_check_data.update({'dts': dts_name, 'temperature': temperatures, 'diode': diode_num,
                                    'voltage_measured': voltage_measured, 'rawcode': rawcode,
                                    'rawcode_calculation': rawcode_calculation, 'error': error})
        print(self.VBE_check_data)
    else:
        self.VBE_check_data_gen1.update({'dts': dts_name, 'temperature': temperatures, 'diode': diode_num,
                                         'voltage_measured': voltage_measured, 'rawcode': rawcode,
                                         'rawcode_calculation': rawcode_calculation, 'error': error})



## CATBLK_VREF_VBE_VCOMP_CHECK ##
def CATBLK_VREF_VBE_VCOMP_CHECK(self):
    codes = [0, 127]
    Asist_Func.dts_disable(self)
    for cattrip_code in codes:
        self.CATBLK_VREF_VBE_VCOMP_data['cattrip_code'].append(cattrip_code)
        Asist_Func.insert_cattrip_code(self, cattrip_code, 0)
        Asist_Func.diode_sel_ovr_en(self)
        Asist_Func.diode_sel_ovr_val(self, 0)
        #  measure comp vref
        Asist_Func.program_viewanasigsel(self, int('0b11010100', 2))
        Asist_Func.dts_enable(self)
        self.CATBLK_VREF_VBE_VCOMP_data['comp_vref'].append(Asist_Func.measure_analog_func(self, 4))
        Asist_Func.dts_disable(self)
        #  measure comp vbe
        Asist_Func.program_viewanasigsel(self, int('0b11010011', 2))
        Asist_Func.dts_enable(self)
        self.CATBLK_VREF_VBE_VCOMP_data['comp_vbe'].append(Asist_Func.measure_analog_func(self, 3))
        Asist_Func.dts_disable(self)
        #  measure vref min
        Asist_Func.program_viewanasigsel(self, int('0b11010001', 2))
        Asist_Func.dts_enable(self)
        self.CATBLK_VREF_VBE_VCOMP_data['vref_min'].append(Asist_Func.measure_analog_func(self, 1))
        Asist_Func.dts_disable(self)
        #  measure vref max
        Asist_Func.program_viewanasigsel(self, int('0b11010010', 2))
        Asist_Func.dts_enable(self)
        self.CATBLK_VREF_VBE_VCOMP_data['vref_max'].append(Asist_Func.measure_analog_func(self, 2))
        Asist_Func.dts_disable(self)
    print(self.CATBLK_VREF_VBE_VCOMP_data)


## ADC Linearity check ##
def DTS_SD_ADC_Linearity_check(self, voltage_step_size):
    Asist_Func.dts_disable(self)
    Asist_Func.adcdfxextvref_select(self, 0)
    Asist_Func.adc_vref_select(self, 3)
    Asist_Func.adc_vref_buf_select(self, 0)
    Asist_Func.adcvinsel0_select(self, 3)
    Asist_Func.anadfxinen_select(self, 2)

    print('Apply external voltage reference to Ivref_a ')
    print('Apply external input voltage  to external pin i_ana_dfx_1')

    Asist_Func.oneshot_disable(self)
    Asist_Func.update_diode_mask(self, 0)
    Asist_Func.dts_enable(self)

    voltage_applied = np.arange(0.1, 0.9, voltage_step_size)
    data = []
    rawcode = []
    for i in range(len(voltage_applied)):
        Asist_Func.apply_voltage_i_ana_dfx_1(voltage_applied[i], 0)
        rawcode.append(Asist_Func.read_temperature_code(self, 0))
        data = [voltage_applied[i], rawcode[i]]
        self.adc_linearity_check.append(data)

    self.adc_slope, self.adc_offset = Asist_Func.calculate_slope_and_offset(voltage_applied, rawcode)
    print('slope: ' + str(self.adc_slope))
    print('offset: ' + str(self.adc_offset))

    ##### maybe export graph?

## ADC Linearity check ##
def DTS_SD_ADC_dynamic_check(self, a):
    frequency_list = [1e3, 10e3, 48e3]
    Asist_Func.dts_disable(self)
    Asist_Func.adcdfxextvref_select(self, 0)
    Asist_Func.adc_vref_select(self, 3)
    Asist_Func.adc_vref_buf_select(self, 0)
    Asist_Func.adcvinsel0_select(self, 3)
    Asist_Func.anadfxinen_select(self, 2)

    print('Apply external voltage reference to Ivref_a ')
    print('Apply external input voltage  to external pin i_ana_dfx_1')
    print('measure the vin with the data logger')

    Asist_Func.oneshot_disable(self)
    Asist_Func.update_diode_mask(self, 0)
    Asist_Func.dts_enable(self)

    for freq in frequency_list:
        start_time =time.time()
        elapsed_time = 0
        target_time = 0.001  # target time in seconds, i.e., 1 millisecond
        while elapsed_time < target_time:
            elapsed_time = time.time() - start_time
            curr_voltage_applied = Asist_Func.measure_analog_func(self, -1)
            rawcode = Asist_Func.read_temperature_code(self, 0)
            data = [freq, elapsed_time, curr_voltage_applied, rawcode]
            self.adc_dynamic_check.append(data)
            time.sleep(0.00001)


## DTS full accuracy function  ##
def DTS_full_accuracy_func(self):
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_pretrim_rawcode_readout_particular_temp(self, temperature)

    # # save the data of pre trim
    # pre_trim_titles = ['dts', 'diode', 'temperature', 'mean_raw_code', 'min_raw_code', 'max_raw_code']
    # for diode in range(self.NumOfDiode):
    #     pre_trim_dict_for_diode = Asist_Func.convert_array_to_dict(self.diodesList[diode].pretrimData, pre_trim_titles)
    #     self.pre_trim_all_diodes_data = Asist_Func.merge_2_dictionaries_with_same_titles(self.pre_trim_all_diodes_data,
    #                                                                                      pre_trim_dict_for_diode)
    Asist_Func.temperature_change(25)
    DTS_trim_rawcode(self)
    for temperature in temperatureList:
        Asist_Func.temperature_change(temperature)
        DTS_posttrim_temp_readout(self, temperature)
    Asist_Func.temperature_change(25)


## Dithering ##
def dithering(self):
    Asist_Func.dithering_enable(self)
    DTS_full_accuracy_func(self)


## AZ DC shift functionality check ##
def AZ_DC_shift_func_check(self):
    Asist_Func.adc_az_offset_en(self)
    DTS_full_accuracy_func(self)


## fusa_check ##
def bgr_fusa_check(self):
    # STEP 1/2/3
    bgrtrimcodes = [self.Step2TrimValue, 11, 21]
    pass_results = [0, 1, 1]
    test_results = [-1, -1, -1]
    for i in range(3):
        Asist_Func.dts_disable(self)
        Asist_Func.oneshot_enable(self)
        Asist_Func.set_any_bg_trim_code(self, bgrtrimcodes[i])
        Asist_Func.update_diode_mask(self, 0)
        Asist_Func.fusa_en(self)
        Asist_Func.fusa_max_thresh(self, 677)
        Asist_Func.fusa_min_thresh(self, 661)
        Asist_Func.dts_enable(self)
        if Asist_Func.bgr_out_of_spec(self) == pass_results[i]:
            test_results[i] = 1  # step passed
        else:
            test_results[i] = 0  # step no passed
    self.fusa_check['dts'].append(self.name)
    self.fusa_check['step_1'].append(test_results[0])
    self.fusa_check['step_2'].append(test_results[1])
    self.fusa_check['step_3'].append(test_results[2])

    print(self.fusa_check)