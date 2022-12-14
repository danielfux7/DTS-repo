## config ##
# Description:
# The function will contain all the global veriabls for all the tests

import pandas as pd

if __name__ == '__main__':
    # data = pd.read_excel(r'C:\Users\daniel\trial.xlsx')
    # print(data)
    #C:\Users\daniel\default.xlsx
    # df = pd.DataFrame(data, columns=['cost'])
    # print(df)
    #
    # cost = list(data.cost)
    # print(cost)
    # name = list(data.name)
    # print(name)
    #
    # res = {name[i] : cost[i] for i in range(len(name))}
    # print(res)

    data = input()
    a = 'r' + "'" + data + "'"
    print(a)
    data = pd.read_excel(input())
    print(data)
