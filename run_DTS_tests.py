import _DTS
from DTS import *
from DTSGEN1 import *
import Asist_Func
from Asist_Func import *
import pickle

if __name__ == '__main__':
    print('Write in the list the DTSs you want to run, the default is all of them-13')
    dts_list = ListAllDTS  # can be modified
    dts_list = ['dts1', 'par_sa_pma0_core0_dts0']  #### for debug
    num_of_tests = 24
    function_status = num_of_tests * [0]
    buf_en_arr = [0, 1]
    bg_wait_time_arr = [0, 0x1ff]  # 0z1ff = 5.12 us
    Asist_Func.insert_calibrated_fuses_to_unit_from_file()
    general_dts = DTS('dts_gen1_gen2')

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
                    '21 - default BGREF check \n 22 - cattrip alert check ext vbe \n 23 - fuses file \n')
        test_num = int(num)
        if -1 < test_num < 20:  # check the name is correct
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
                    for bgwait in bg_wait_time_arr:
                        DTS_dict[dts].DTS_full_accuracy_func(bgwait)
                else:
                    for buf_en in buf_en_arr:
                        DTS_dict[dts].DTS_full_accuracy_func_gen1(buf_en)
            Asist_Func.write_slope_offset_to_file()


        ## cattrip calibration ##
        elif test_num == 4:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_full_cattrip_calib_func()
                else:
                    for buf_en in buf_en_arr:
                        DTS_dict[dts].DTS_full_cattrip_calib_func_gen1()
            Asist_Func.write_cattripcode_to_file()


        ## sleep delay check ##
        elif test_num == 5:
            print('This test only for gen2')
            sleep_time = 1  # TBD check what should be the time?
            sleepTimeDynamic = 2  # TBD check what should be the time?
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].SLEEP_DELAY_CHECK(sleep_time, sleepTimeDynamic)


        ## BG wait time check ##
        elif test_num == 6:
            print('This test only for gen2')
            bg_wait = 500  # can be something that bigger than 300 and can be observed
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].BG_WAIT_TIME_CHECK(bg_wait)


        ## ADC clock divider test ##
        elif test_num == 7:
            print('This test only for gen2')
            diode = 0  # can be modified
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    for temperature in temperatureList:
                        Asist_Func.temperature_change(temperature)
                        DTS_dict[dts].ADC_CLK_DIV_TEST(temperature, diode)


        ## AON override DTS func check ##
        elif test_num == 8:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].AON_OVRD_DTS_FUNC_CHECK()


        ## DTD NS alert test ##
        elif test_num == 9:
            print('This test only for gen2')
            maxTemperature = 50
            minTemperature = 40
            threshold = 45
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    direction = 1
                    DTS_dict[dts].DTD_NS_ALERT_TEST( maxTemperature, minTemperature, threshold, direction)
                    direction = 0
                    DTS_dict[dts].DTD_NS_ALERT_TEST( maxTemperature, minTemperature, threshold, direction)


        ## DTD sticky alert test ##
        elif test_num == 10:
            print('This test only for gen2')
            maxTemperature = 70
            minTemperature = 54
            lowLimit = 57
            highLimit = 67
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTD_STICKY_ALERT_TEST(maxTemperature, minTemperature, lowLimit, highLimit)


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
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_PRETRIM_BGREF_CHECK()


        ## ANA power up sequence view ##
        elif test_num == 13:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].ANA_PWR_SEQ_VIEW()


        ## dithering ##     ######## need to finish
        elif test_num == 14:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].dithering()


        ## RD VBE check ##    ######## need to finish
        elif test_num == 15:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_RD_VBE_Check()
                else:
                    DTS_dict[dts].PWRON_DTS_RD_VBE_Check()


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


        ## fusa check ##
        elif test_num == 19:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].bgr_fusa_check()


        ## post trim BGREF check ##
        elif test_num == 20:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_POSTTRIM_BGREF_CHECK()


        ## default trim BGREF check ##
        elif test_num == 21:
            print('This test only for gen2')
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_DEFAULT_BGREF_CHECK()


        ## cattrip alert check ext vbe ##
        elif test_num == 22:
            print('This test only for gen1')
            for dts in dts_list:
                if DTS_dict[dts].gen == 1:
                    DTS_dict[dts].DTS_CATTRIP_ALERT_CHK_EXTVBE()

        ## fuses file ##
        elif test_num == 23:
            Asist_Func.export_all_fuses_from_unit_to_file()