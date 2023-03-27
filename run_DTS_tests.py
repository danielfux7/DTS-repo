import _DTS
from DTS import *
from DTSGEN1 import *
import Asist_Func
from Asist_Func import *
import pickle

if __name__ == '__main__':
    print('Write in the list the DTSs you want to run, the default is all of them-13')
    dts_list = ListAllDTS  # can be modified
    dts_list = ['dts1', 'atom_lpc']  #### for debug
    num_of_tests = 5
    function_status = 5 * [0]
    buf_en_arr = [0, 1]
    bg_wait_time_arr = [0]  # need to check what time I need to put

    # Choose what tests to run
    while 1:
        print('Choose the DTS for the tests from the list:')
        num = input('Press the number of the test to run:\n 0 - declare DTSs \n 1 - fuses_check \n 2 - BGR calibration '
                    '\n 3 - pre and post trim \n 4 - cattrip calibration \n 5 - another tests \n')
        test_num = int(num)
        if -1 < test_num < 5:  # check the name is correct
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
        if test_num == 1:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    DTS_dict[dts].DTS_TAP_Default_Check()
                    DTS_dict[dts].DTS_CRI_Default_Check()
                else:
                    DTS_dict[dts].DTS_GEN1_TAP_DEFAULT_CHECK()


        ## BGR calibration ##
        if test_num == 2:
            for dts in dts_list:
                if DTS_dict[dts].gen == 1:
                    continue

                DTS_dict[dts].bg_trim_step1()
                DTS_dict[dts].bg_trim_step2()


        ## pre and post trim ##
        if test_num == 3:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    for bgwait in bg_wait_time_arr:
                        DTS_dict[dts].DTS_full_accuracy_func(bgwait)
                else:
                    for buf_en in buf_en_arr:
                        DTS_dict[dts].DTS_full_accuracy_func_gen1(buf_en)

        ## cattrip calibration ##
        if test_num == 4:
            for dts in dts_list:
                if DTS_dict[dts].gen == 2:
                    for bgwait in bg_wait_time_arr:
                        DTS_dict[dts].DTS_full_accuracy_func(bgwait)
                else:
                    for buf_en in buf_en_arr:
                        DTS_dict[dts].DTS_full_accuracy_func_gen1(buf_en)