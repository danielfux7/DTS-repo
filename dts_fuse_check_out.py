import _DTS
from DTS import *
from DTSGEN1 import *


if __name__ == '__main__':
    print('The input of this functions is the path to the excel that contain all the tap commands for all \n'
          'the dts fuses -the column name is "name" \n'
          'and another column with all the default values - the'
          'column name is "value" \n')

    # C:\Users\daniel\default_values_final.xlsx
    final_excel_file_dict = {'name': [], 'default_values': [], 'fuse_values': [], 'statues': []}
    path = input('insert the full path to the default values \n')
    export_path = create_new_path_for_excel(path, 'dts_fuse_checkout')
    default_data = pd.read_excel(path)
    default_names = list(default_data.name)
    default_values = list(default_data.value)

    for i in range(len(default_names)):
        command = 'cpu.' + default_names[i]
        fuse_value = eval(command)
        if fuse_value != int(default_values[i], 16):
            statues = False
        else:
            statues = True

        # save data
        final_excel_file_dict['name'].append(default_names[i])
        final_excel_file_dict['default_values'].append(default_values[i])
        final_excel_file_dict['fuse_values'].append(fuse_value)
        final_excel_file_dict['statues'].append(statues)

    df = pd.DataFrame.from_dict(final_excel_file_dict)
    df.to_excel(export_path)