import pandas as pd
import numpy as np

ListDTS = ['dts0_aon', 'dts1', 'dts2', 'dts3', 'dts_ccf0', 'dts_ccf1', 'dts_gt0', 'dts_gt1']
ListDTSGen1 = ['par_sa_pma0_core0_dts0', 'par_sa_pma0_core1_dts0', 'par_sa_pma1_core0_dts0', 'par_sa_pma1_core1_dts0', 'atom_lpc']
commandSuffix = 'cdie.taps.cdie_'


if __name__ == '__main__':

    # GEN2 Export
    partData = pd.read_excel(r'C:\Users\daniel\dts_fuses.xlsx')
    partName = list(partData.FuseName)
    partValue = list(partData.defaultval)

    #  Filtering the fields :
    for i in range(len(partValue)):
        string = partValue[i]
        index = string.find('h')
        partValue[i] = string[index + 1:]

    fullName = []
    value = []
    for dts in ListDTS:
        for i in range(len(partName)):
            name = commandSuffix + dts + '.dtsfusecfg.' + str(partName[i])
            fullName.append(name)
            value.append(partValue[i])

    finalDict = {'name': fullName, 'value': value}
    print('check')
    # print(finalDict['cdie.taps.cdie_dts2.dtsfusecfg.adcvinsel0'])

    # Convert the dictionaries to dataframes
    df = pd.DataFrame(finalDict)

    # Export the dataframe to an Excel file
    df.to_excel(r'C:\Users\daniel\fuse_list_gen2.xlsx')

    # GEN1 Export
    partData = pd.read_excel(r'C:\Users\daniel\dts_fuses_gen1.xlsx')
    partName = list(partData.FuseName)
    partValue = list(partData.defaultval)

    #  Filtering the fields :
    for i in range(len(partValue)):
        string = partValue[i]
        index = string.find('h')
        if index < 0:
            continue
        partValue[i] = string[index + 1:]

    fullName = []
    value = []
    for dts in ListDTSGen1:
        for i in range(len(partName)):
            name = commandSuffix + dts + '.dtsfusecfg.' + str(partName[i])
            fullName.append(name)
            value.append(partValue[i])

    finalDict = {'name': fullName, 'value': value}
    print('check')
    # print(finalDict['cdie.taps.cdie_dts2.dtsfusecfg.adcvinsel0'])

    # Convert the dictionaries to dataframes
    df = pd.DataFrame(finalDict)

    # Export the dataframe to an Excel file
    df.to_excel(r'C:\Users\daniel\fuse_list_gen1.xlsx')