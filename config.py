## config ##
# Description:
# The function will contain all the global veriabls for all the tests

import pandas as pd
from pathlib import Path

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

    # data = input()
    # a = 'r' + "'" + data + "'"
    # print(a)
    data1 = pd.read_excel(r'C:\Users\daniel\trial.xlsx')
    data2 = pd.read_excel(r'C:\Users\daniel\trial1.xlsx')
    print(data1)
    print(data2)
    data1.name = data1.name.astype(str)
    data1.default_value = data1.default_value.astype(str)
    data2.name = data2.name.astype(str)
    data2.unit_value = data2.unit_value.astype(str)

    data1.name = data1.name.str.strip()
    data1.default_value = data1.default_value.str.strip()
    data2.name = data2.name.str.strip()
    data2.unit_value = data2.unit_value.str.strip()
    a = data1.merge(data2, left_on='name', right_on='name')
    print(a)
 #   path = '/Users/daniel/trial.xlsx'
#    b = 'C:\Users\daniel\trial.xlsx'
  ##  print(b)
    #a.to_excel(r'C:\Users\daniel\out.xlsx')
    # print('final:')
    # print(data1)
    # print(data2)
    #
    # df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
    #                     'value': [1, 2, 3, 5]})
    # df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
    #                     'value': [5, 6, 7, 8]})
    # print(df1.merge(df2, left_on='lkey', right_on='rkey'))




