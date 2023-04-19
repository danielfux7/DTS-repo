import _DTS
from DTS import *
from DTSGEN1 import *


if __name__ == '__main__':
    print('The input of this function are 2 excel file with all the field names and values,'
          ' one for gen2 and another for gen1 \n'
          'when the name of the column is "name" \n')
    # C:\Users\daniel\fuses_gen1.xlsx
    # C:\Users\daniel\fuses_gen2.xlsx
    final_excel_file_dict = {'name': [], 'value': []}
    # gen2 prep
    path_gen2 = input('insert the full path to the gen2 fields \n')
    gen2_data = pd.read_excel(path_gen2)
    gen2_names = list(gen2_data.name)
    # gen1 prep
    path_gen1 = input('insert the full path to the gen1 fields \n')
    gen1_data = pd.read_excel(path_gen1)
    gen1_names = list(gen1_data.name)

    # save the data for gen2
    for dts in ListDTS:
        for i in range(len(gen2_data)):
            name = 'cdie.taps.cdie_' + dts + '.dtsfusecfg.' + gen2_names[i]
            command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.' + gen2_names[i]
            value = eval(command)
            final_excel_file_dict['name'].append(name)
            final_excel_file_dict['value'].append(value)

    # save the data for gen1
    for dts in listGEN1DTS:
        for i in range(len(gen1_data)):
            if dts != 'atom_lpc':
                name = 'cdie.taps.cdie_' + dts + '.dtsfusecfg.' + gen1_names[i]
                command = 'cpu.cdie.taps.cdie_' + dts + '.dtsfusecfg.' + gen1_names[i]
            else:
                name = 'cdie.taps.cdie_' + dts + '.dtstapcfgfuse.' + gen1_names[i]
                command = 'cpu.cdie.taps.cdie_' + dts + '.dtstapcfgfuse.' + gen1_names[i]
            value = eval(command)
            final_excel_file_dict['name'].append(name)
            final_excel_file_dict['value'].append(value)

    export_path = create_new_path_for_excel(path_gen2, 'all_dts_names_and_values')
    df = pd.DataFrame.from_dict(final_excel_file_dict)
    df.to_excel(export_path)

