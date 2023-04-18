import _DTS
from DTS import *
from DTSGEN1 import *


if __name__ == '__main__':
    for dts in ListAllDTS:
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
            print(dts_gen1.name)
    catastrophic_dict = {'sensor': []}
    path = r'C:\Users\daniel\results\catastrophic_point_check.xlsx'
    temperatures = []
    iteration = 1
    flag = 1
    input('Start to increase the temperature to 130 and than press any key to continue')
    while True:
        iteration_name = 'iteration: ' + str(iteration)
        catastrophic_dict[iteration_name] = []
        for dts in ListAllDTS:
            for diode in range(DTS_dict[dts].NumOfDiode):
                if flag: # create the names only in the first iteration
                    sensor_name = dts + '_' + str(diode)
                    catastrophic_dict['sensor'].append(sensor_name)
                curr_temperature = Asist_Func.read_temperature_code(DTS_dict[dts], diode)
                catastrophic_dict[iteration_name].append(curr_temperature)
        df = pd.DataFrame.from_dict(catastrophic_dict)
        df.to_excel(path)
        print(catastrophic_dict)
        iteration += 1
        flag = 0
