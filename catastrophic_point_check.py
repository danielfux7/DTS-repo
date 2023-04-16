import _DTS
from DTS import *
from DTSGEN1 import *

dts_list =
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
            # print(dts_gen1.name)
    while True:
        
