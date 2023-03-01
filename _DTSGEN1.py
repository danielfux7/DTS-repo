import Asist_Func
from Asist_Func import *
import Diode
from Diode import *


def __init__(self):

    while 1:
        print('Choose the DTS for the tests from the list:')
        name = input('Press the number of the GEN1 DTS: \n 0 - DTS core0 \n')
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