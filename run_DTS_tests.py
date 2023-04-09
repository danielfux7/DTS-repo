import _DTS
from DTS import *
from DTSGEN1 import *
import Asist_Func
from Asist_Func import *
import pickle

if __name__ == '__main__':
    print('Write in the list the DTSs you want to run, the default is all of them-13')
    dts_list = ListAllDTS  # can be modified
    dts_list = ['dts1', 'dts2', 'par_sa_pma0_core0_dts0']  #### for debug
    num_of_tests = 25
    function_status = num_of_tests * [0]
    buf_en_arr = [0, 1]
    bg_wait_time_arr = [0]  # 0z1ff = 5.12 us
    Asist_Func.insert_calibrated_fuses_to_unit_from_file()
    general_dts = DTS('dts')

    # Choose what tests to run
    while 1:
        print('Choose the DTS for the tests from the list:')
        num = input('Press the number of the test to run:\n 0 - declare DTSs \n 1 - fuses_check \n 2 - BGR calibration '
                    '\n 3 - pre and post trim \n 4 - cattrip calibration \n 5 - sleep delay check(also dynamic) \n '
                    '6 - BG wait time check \n 7 - ADC clock divider test \n 8 - AON override DTS func check \n '
                    '9 - DTD NS alert test \n 10 - DTD sticky alert test \n 11 - power up output glitch check \n '
                    '12 - pre trim BGREF check \n 13 - ANA power up sequence view \n 14 - dithering \n '
                    '15 - RD VBE check \n 16 - CATBLK VREF VBE VCOMP check \n 17 - ADC linearity check \n '
                    '18 - AZ DC shift functionality check \n 19 - fusa check \n 20 - post trim BGREF check \n '
                    '21 - default BGREF check \n 22 - cattrip alert check ext vbe \n 23 - fuses file \n'
                    ' 24 - bg wait raw code check \n')
        test_num = int(num)
        if -1 < test_num < 25:  # check the name is correct
            if function_status[test_num]:
                ans = input('are you sure you want to repeat this test? press y/n \n')
                if ans == 'n':
                    continue
        function_status[test_num] = 1

        # DTSs declaration
        if test_num == 0:
            after_test_DTS = []
            for dts in dts_list:
                if dts in ListDTS:  # check if gen2 dts
                    dts_gen2 = DTS(dts)
                    DTS_dict[dts] = dts_gen2
                    gen = 2
                    # print(dts_gen2.name)
                    # print(DTS_dict['dts2'].name)
                else:
                    dts_gen1 = DTSGEN1(dts)
                    DTS_dict[dts] = dts_gen1
                    gen = 1
                    #print(dts_gen1.name)

        ## Fuses check ##
        elif test_num == 1:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_TAP_Default_Check()
                    DTS_dict[dts].DTS_CRI_Default_Check()
                else:
                    DTS_dict[dts].DTS_GEN1_TAP_DEFAULT_CHECK()


        ## BGR calibration ##
        elif test_num == 2:
            bgrtrimcode_dict = {'DTS': [], 'bgrtrimcode': []}
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 1:
                    DTS_dict[dts].BGR_calib_gen1(63)
                    bgrtrimcode_dict['DTS'].append(dts)
                    bgrtrimcode_dict['bgrtrimcode'].append(DTS_dict[dts].bgrtrimcode)
                    continue

                DTS_dict[dts].bg_trim_step1()
                DTS_dict[dts].bg_trim_step2()
                bgrtrimcode_dict['DTS'].append(dts)
                bgrtrimcode_dict['bgrtrimcode'].append(DTS_dict[dts].Step2TrimValue)
            Asist_Func.write_calibrated_bgtrim_code_to_file()
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'BGR_calibration', bgrtrimcode_dict)


        ## pre and post trim ##
        elif test_num == 3:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_full_accuracy_func()
                else:
                    for buf_en in buf_en_arr:
                        DTS_dict[dts].DTS_full_accuracy_func_gen1(buf_en)
            Asist_Func.write_slope_offset_to_file()
            Asist_Func.export_full_accuracy_data(general_dts, dts_list, 0)


        ## cattrip calibration ##
        elif test_num == 4:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_full_cattrip_calib_func()
                else:
                    DTS_dict[dts].DTS_full_cattrip_calib_func_gen1()
            Asist_Func.write_cattripcode_to_file()
            Asist_Func.export_full_cattrip_data(general_dts, dts_list)


        ## sleep delay check ##
        elif test_num == 5:
            print('This test only for gen2')
            sleep_delay_dict = {'DTS_name': [], 'time_expected': [], 'time_measured': [], 'diff_time': [],
                                'time_expected_dynamic': [], 'time_measured_dynamic': [], 'diff_dyn_time': []}
            sleep_time = 1  # TBD check what should be the time?
            num = input('For sleep delay check press - 0 \n'
                        'For dynamic delay check insert the time \n')
            sleepTimeDynamic = int(num)
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].SLEEP_DELAY_CHECK(sleep_time, sleepTimeDynamic)
                    sleep_delay_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        sleep_delay_dict, DTS_dict[dts].sleep_delay_check_data)
            if sleepTimeDynamic:
                test_name = 'dynamic_sleep_delay_check'
            else:
                test_name = 'sleep_delay_check'
            Asist_Func.create_excel_file_for_chosen_func(general_dts, test_name, sleep_delay_dict)
            general_dts.sleep_delay_check_data = sleep_delay_dict


        ## BG wait time check ##
        elif test_num == 6:
            bg_wait_dict = {'DTS_name': [], 'time_expected': [], 'time_measured': [], 'diff_time': []}
            print('This test only for gen2')
            bg_wait = 500  # can be something that bigger than 300 and can be observed
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].BG_WAIT_TIME_CHECK(bg_wait)
                    bg_wait_dict = Asist_Func.merge_2_dictionaries_with_same_titles(bg_wait_dict,
                                                                                    DTS_dict[dts].bg_wait_time_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'BG_wait_check', bg_wait_dict)
            general_dts.bg_wait_time_data = bg_wait_dict


        ## ADC clock divider test ##
        elif test_num == 7:
            adc_clk_div_dict = {'DTS_name': [], 'frequency': [], 'temperature': [],
                                'measured_temperature': [], 'error': []}
            print('This test only for gen2')
            diode = 0  # can be modified
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    for temperature in temperatureList:
                        Asist_Func.temperature_change(temperature)
                        DTS_dict[dts].ADC_CLK_DIV_TEST(temperature, 0)
                        adc_clk_div_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                            adc_clk_div_dict,DTS_dict[dts].adc_clk_all_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'ADC_clock_divider', adc_clk_div_dict)
            general_dts.adc_clk_all_data = adc_clk_div_dict


        ## AON override DTS func check ##
        elif test_num == 8:
            aon_override_dict = {'dts': [], 'OSR_mode': [], 'diode': [], 'temperature': [],
                                 'measured_temperature': [], 'error': []}
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].AON_OVRD_DTS_FUNC_CHECK()
                    aon_override_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        aon_override_dict, DTS_dict[dts].post_trim_all_diodes_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'AON_override_dts_func_check', aon_override_dict)


        ## DTD NS alert test ##  #### need to finish the excel data
        elif test_num == 9:
            print('This test only for gen2')
            dtd_ns_alert_direction_0_dict = {'dts': [], 'thresh_hold': [], 'temperature_alert_generated': [],
                                             'diff_part_a': [], 'pass_part_a': [], 'temperature_alert_gone': [],
                                             'diff_part_b': [], 'pass_part_b': []}
            dtd_ns_alert_direction_1_dict = {'dts': [], 'thresh_hold': [], 'temperature_alert_generated': [],
                                             'diff_part_a': [], 'pass_part_a': [], 'temperature_alert_gone': [],
                                             'diff_part_b': [], 'pass_part_b': []}
            maxTemperature = 50
            minTemperature = 40
            threshold = 45
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    direction = 1
                    DTS_dict[dts].DTD_NS_ALERT_TEST(maxTemperature, minTemperature, threshold, direction)
                    dtd_ns_alert_direction_1_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        dtd_ns_alert_direction_1_dict, DTS_dict[dts].DTD_NS_alert_direction_1_data)
                    direction = 0
                    DTS_dict[dts].DTD_NS_ALERT_TEST(maxTemperature, minTemperature, threshold, direction)
                    dtd_ns_alert_direction_0_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        dtd_ns_alert_direction_0_dict, DTS_dict[dts].DTD_NS_alert_direction_0_data)
            Asist_Func.create_excel_file_for_chosen_func(
                general_dts, 'dtd_ns_alert_direction_0_test', dtd_ns_alert_direction_0_dict)
            Asist_Func.create_excel_file_for_chosen_func(
                general_dts, 'dtd_ns_alert_direction_1_test', dtd_ns_alert_direction_1_dict)


        ## DTD sticky alert test ## #### need to finish the excel data
        elif test_num == 10:
            print('This test only for gen2')
            dtd_sticky_alert_dict = {'dts': [], 'thresh_hold_high': [], 'temperature_alert_generated_high': [],
                                     'diff_part_a': [], 'sticky_alert_part_a': [], 'pass_part_a': [],
                                     'thresh_hold_low': [], 'temperature_alert_generated_low': [], 'diff_part_b': [],
                                     'sticky_alert_part_b': [], 'pass_part_b': []}
            maxTemperature = 70
            minTemperature = 54
            lowLimit = 57
            highLimit = 67
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTD_STICKY_ALERT_TEST(maxTemperature, minTemperature, lowLimit, highLimit)
                    Asist_Func.merge_2_dictionaries_with_same_titles(dtd_sticky_alert_dict,
                                                                     DTS_dict[dts].DTD_sticky_alert_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'dtd_sticky_alert_test', dtd_sticky_alert_dict)


        ## power up output glitch check ##     ######## need discuss with Michael!
        elif test_num == 11:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    pass
                    #DTS_dict[dts].


        ## pre trim BGREF check ##    ######## need to finish the data saving
        elif test_num == 12:
            print('This test only for gen2')
            pre_trim_bgref_dict = {'dts': [], 'tc': [], 'vtrim_700m': []}
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_PRETRIM_BGREF_CHECK()
                    pre_trim_bgref_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        pre_trim_bgref_dict, DTS_dict[dts].pre_trim_bg_ref_data)
            create_excel_file_for_chosen_func(general_dts, 'pre_trim_bgref_check', pre_trim_bgref_dict)
            general_dts.pre_trim_bg_ref_data = pre_trim_bgref_dict

        ## ANA power up sequence view ##
        elif test_num == 13:
            print('This test only for gen2')
            ana_pwr_seq_dict = {'power_gate_enable': [], 'BGR_enable': [], 'LDO1p2V_enabled': [],
                                'ADC_sup_buf_enable': [], 'ADC_sup_buf_enable_delayed': []}
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].ANA_PWR_SEQ_VIEW()
                    ana_pwr_seq_dict = Asist_Func.merge_2_dictionaries_with_same_titles(ana_pwr_seq_dict,
                                                                                        DTS_dict[dts].ana_pwr_seq_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'ana_pwr_seq_view', ana_pwr_seq_dict)
            general_dts.ana_pwr_seq_data = ana_pwr_seq_dict

        ## dithering ##
        elif test_num == 14:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].dithering()
            Asist_Func.export_full_accuracy_data(general_dts, dts_list, 'dithering')


        ## RD VBE check ##
        elif test_num == 15:
            VBE_check_dict = {'dts': [], 'temperature': [], 'diode': [], 'voltage_measured': [], 'rawcode': [],
                              'rawcode_calculation': [], 'error': []}
            VBE_check_gen1_dict = {'dts': [], 'temperature': [], 'diode': [], 'voltage_measured': [], 'rawcode': [],
                                   'rawcode_calculation': [], 'error': []}
            temperatures_list_for_RD_VBE_check = [30, 80]
            for dts in dts_list:
                for temperature in temperatures_list_for_RD_VBE_check:
                    if DTS_dict[dts].gen == 2:
                        DTS_dict[dts].DTS_RD_VBE_Check(temperature)
                        Asist_Func.merge_2_dictionaries_with_same_titles(VBE_check_dict, DTS_dict[dts].VBE_check_data)
                    else:
                        DTS_dict[dts].PWRON_DTS_RD_VBE_Check(temperature)
                        Asist_Func.merge_2_dictionaries_with_same_titles(VBE_check_dict,
                                                                         DTS_dict[dts].VBE_check_data_gen1)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'RD_VBE_check', VBE_check_dict)
            general_dts.VBE_check_data = VBE_check_dict


        ## CATBLK VREF VBE VCOMP check ##    ######## need to finish
        elif test_num == 16:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].CATBLK_VREF_VBE_VCOMP_CHECK()


        ## ADC linearity check ##    ######## need to finish for gen 1!
        elif test_num == 17:
            voltage_step_size = 0.09
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_SD_ADC_Linearity_check( voltage_step_size)
                else:
                    DTS_dict[dts].DTS_ADC_Linearity_check()


        ## AZ DC shift functionality check ##
        elif test_num == 18:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].AZ_DC_shift_func_check()
            Asist_Func.export_full_accuracy_data(general_dts, dts_list, 'az_dc_shift_check')

        ## fusa check ##
        elif test_num == 19:
            print('This test only for gen2')
            bgr_fusa_dict = {'dts': [], 'step_1': [], 'step_2': [], 'step_3': []}
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].bgr_fusa_check()
                    bgr_fusa_dict = Asist_Func.merge_2_dictionaries_with_same_titles(bgr_fusa_dict,
                                                                                     DTS_dict[dts].fusa_check)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'bgr_fusa_check', bgr_fusa_dict)
            general_dts.fusa_check = bgr_fusa_dict


        ## post trim BGREF check ##
        elif test_num == 20:
            print('This test only for gen2')
            post_trim_bgref_dict = {'dts': [], 'tc': [], 'vtrim_700m': []}
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_POSTTRIM_BGREF_CHECK()
                    post_trim_bgref_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        DTS_dict[dts].post_trim_bg_ref_data, post_trim_bgref_dict)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'post_trim_bgref_check', post_trim_bgref_dict)
            general_dts.post_trim_bg_ref_data = post_trim_bgref_dict


        ## default trim BGREF check ##
        elif test_num == 21:
            print('This test only for gen2')
            default_bgref_dict = {'dts': [], 'tc': [], 'vtrim_700m': []}
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_DEFAULT_BGREF_CHECK()
                    default_bgref_dict = Asist_Func. merge_2_dictionaries_with_same_titles(
                        default_bgref_dict, DTS_dict[dts].bg_ref_default_check_data)
            Asist_Func.create_excel_file_for_chosen_func(general_dts, 'default_trim_bgref_check', default_bgref_dict)
            general_dts.bg_ref_default_check_data = default_bgref_dict

        ## cattrip alert check ext vbe ##
        elif test_num == 22:
            print('This test only for gen1')
            for dts in dts_list:
                if DTS_dict[dts].gen == 1:
                    DTS_dict[dts].DTS_CATTRIP_ALERT_CHK_EXTVBE()

        ## fuses file ##
        elif test_num == 23:
            Asist_Func.export_all_fuses_from_unit_to_file()

        ## bg wait code check ##
        elif test_num == 24:
            print('This test only for gen2')
            bg_wait_code_dict = {'dts': [], 'diode': [], 'temperature': [], 'mean_raw_code': [],
                                 'mean_raw_code_bg_wait': [], 'min_raw_code': [], 'min_raw_code_bg_wait': [],
                                 'max_raw_code': [], 'max_raw_code_bg_wait': []}
            pre_trim_dict = {'dts': [], 'diode': [], 'temperature': [], 'mean_raw_code': [],
                             'min_raw_code': [], 'max_raw_code': []}
            bg_wait_code_temperature_list = [10, 25, 50, 75, 100, 125]
            bg_wait_time_list = [0x1ff]
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].pre_trim_all_diodes_data = {'dts': [], 'diode': [],
                                                              'temperature': [], 'mean_raw_code': [],
                                                              'min_raw_code': [], 'max_raw_code': []}
                    for temperature in bg_wait_code_temperature_list:
                        Asist_Func.temperature_change(temperature)
                        DTS_dict[dts].pretrim_rawcode_readout(temperature)
                    pre_trim_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                        pre_trim_dict, DTS_dict[dts].pre_trim_all_diodes_data)
            # save the data on bg
            bg_wait_code_dict['dts'] = pre_trim_dict['dts']
            bg_wait_code_dict['diode'] = pre_trim_dict['diode']
            bg_wait_code_dict['temperature'] = pre_trim_dict['temperature']
            bg_wait_code_dict['mean_raw_code'] = pre_trim_dict['mean_raw_code']
            bg_wait_code_dict['min_raw_code'] = pre_trim_dict['min_raw_code']
            bg_wait_code_dict['max_raw_code'] = pre_trim_dict['max_raw_code']

            pre_trim_dict = {'dts': [], 'diode': [], 'temperature': [], 'mean_raw_code': [],
                             'min_raw_code': [], 'max_raw_code': []}
            for bg_wait in bg_wait_time_list:
                for dts in dts_list:
                    if DTS_dict[dts].gen == 2:
                        DTS_dict[dts].pre_trim_all_diodes_data = {'dts': [], 'diode': [],
                                                                  'temperature': [], 'mean_raw_code': [],
                                                                  'min_raw_code': [], 'max_raw_code': []}
                        for temperature in bg_wait_code_temperature_list:
                            Asist_Func.temperature_change(temperature)
                            Asist_Func.dts_disable(DTS_dict[dts])
                            Asist_Func.program_bg_wait(DTS_dict[dts], bg_wait)
                            DTS_dict[dts].pretrim_rawcode_readout(temperature)
                        pre_trim_dict = Asist_Func.merge_2_dictionaries_with_same_titles(
                            pre_trim_dict, DTS_dict[dts].pre_trim_all_diodes_data)

                # save the rest of the data
                bg_wait_code_dict['mean_raw_code_bg_wait'] = pre_trim_dict['mean_raw_code']
                bg_wait_code_dict['min_raw_code_bg_wait'] = pre_trim_dict['min_raw_code']
                bg_wait_code_dict['max_raw_code_bg_wait'] = pre_trim_dict['max_raw_code']
                Asist_Func.create_excel_file_for_chosen_func(general_dts, 'bg_wait_code_check_' + str(bg_wait),
                                                             bg_wait_code_dict)
                general_dts.bg_wait_code_data = bg_wait_code_dict
