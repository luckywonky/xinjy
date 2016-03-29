import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from dateutil.parser import parse
data = 'f.xlsx'
df = pd.read_excel(data)
l1 = list(df['借款人'])
l2 = []
l3 = []
[l2.append(i) for i in l1 if not i in l2]
def getnofaxi():
    for i in l2:
        gerenjiekuan = df[df['借款人'] == i]
        if(sum(gerenjiekuan['待偿罚息']) + sum(gerenjiekuan['已偿罚息'])) > 0:
            l3.append(i)
    for i in l3:
        l2.remove(i)
#get a new dataframe with no faxi
    index1 = []
    for i in df.index:
        if(df['借款人'][i] in l2):
            index1.append(i)
    nofaxi = df.loc[index1]
    return nofaxi
result1 = getnofaxi()
#print(result1)

def getaftertime(df = result1):
    l = []
    for i in df.index:
        time = parse(df.loc[i]['贷款生效日期'])
        if time - parse('2015-11-10') > timedelta(0):
            l.append(i)
    return df.loc[l]
result2 = getaftertime()

def quchudaihuankuan(df=result2):
    noweihuankuan = pd.DataFrame()
    l4 = list(df['借款人'])
    l5 = []
    [l5.append(i) for i in l4 if not i in l5]
    for i in l5:
        gerenjiekuan = df[df['借款人'] == i]
        for j in gerenjiekuan.index:
            if gerenjiekuan.loc[j]['贷款状态'] == '已还款':
                noweihuankuan = noweihuankuan.append(gerenjiekuan.loc[j])
            else:
                break
    kuanshu = {}
    for i in noweihuankuan.index:
        if noweihuankuan['借款人'][i] not in kuanshu:
            kuanshu[noweihuankuan['借款人'][i]] = 0
        kuanshu[noweihuankuan['借款人'][i]] +=1
    for i in kuanshu.keys():
        if kuanshu[i] == 1:
            for j in noweihuankuan.index:
                if noweihuankuan['借款人'][j] == i:
                    noweihuankuan = noweihuankuan.drop(j)
    return noweihuankuan
result3 = quchudaihuankuan()
    #return noweihuankuan
def getpropertime(df = result3):
    # 去除不是30- 90 天的
    for i in df.index:
        t = parse(df['合同还款日期'][i]) - parse(df['贷款生效日期'][i])
        if (t > timedelta(180)) | (t < timedelta(30)):
            df = df.drop(i)
    #print(df)
    # 选择下一笔借款时上一笔借款已还清的
    l6 = list(df['借款人'])
    l7 = []
    l8 = []
    [l7.append(i) for i in l6 if not i in l7]
    meirenrenkuanshu = {}
    for i in l7:
        gerenjiekuan = df[df['借款人'] == i]
        for j in gerenjiekuan.index:
            if df['借款人'][j] not in meirenrenkuanshu.keys():
                meirenrenkuanshu[df['借款人'][j]] = 0
            meirenrenkuanshu[df['借款人'][j]] += 1
            if (meirenrenkuanshu[df['借款人'][j]] == 2):
                        if parse(df['贷款生效日期'][j]) > (parse(df['贷款生效日期'][j-1]) + timedelta(df['资金使用天数'][j-1])):
                            l8.append(df['借款人'][j])
    print(l8)
    # 去除l8中重复的
    l9 = []
    [l9.append(i) for i in l8 if not i in l9]
    print(l9)
    index1 = []
    for i in df.index:
        if(df['借款人'][i] in l9):
            index1.append(i)
    df = df.loc[index1]
   # df.columns = ['合同编号', '借款人', '贷款生效日期', '贷款金额', '待偿还本金', '资金使用天数', '利率', '待偿还利息','已偿利息', '待偿罚息', '已偿罚息', '合同还款日期', '贷款状态']
    return df
result4 = getpropertime()
result4.to_excel('3.xlsx')
print(result4)













