#作业调度算法的实现，实时版
#created by cupcdown
#2019-6-10

import pandas as pd
from pandas import DataFrame
import copy
import time
import datetime

#空转
def idle(wpd):
    return -1

#读取文件
def read_date(str):
    label=pd.read_csv(str,engine="python")  #windows下读取要加参数engin="python"
    df=DataFrame(label)             #读取csv中数据
    result_list=[]
    for i in range(df.shape[0]):    #转换为列表list
        result_list.append([])
        result_list[i].append(df.iloc[i]['name'])
        result_list[i].append(df.iloc[i]['start'])
        result_list[i].append(int(df.iloc[i]['time']))
    return result_list

#计算响应比
def compute_RN(start_time,work_time):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%H:%M:%S')          #获取当前时间
    d1 = datetime.datetime.strptime(start_time, '%H:%M:%S')
    d2 = datetime.datetime.strptime(now_time, '%H:%M:%S')
    return 1+(d2-d1).seconds/work_time               #计算响应比

#先来先服务，输入等待处理的数据列表
def FCFS(wpd):
    if wpd==[]:
        return -1
    else:
        result=wpd[0]
        result.append(compute_RN(wpd[0][1],wpd[0][2]))
        wpd.pop(0)              #删除执行完的作业
        return result

#最短服务优先
def SJF(wpd):
    if wpd==[]:
        return -1
    else:
        min=65535
        index=-1
        for j in range(len(wpd)):  #找出最短时间的作业
            if min>wpd[j][2]:
               index=j
               min=wpd[j][2]
        result=wpd[index]
        result.append(compute_RN(wpd[index][1],wpd[index][2]))
        wpd.pop(index)
        return result

#最高响应比优先
def HRN(wpd):
    if wpd==[]:
        return -1
    else:
        max=-1
        index=-1
        for j in range(len(wpd)):             #查找最高响应比的作业
            now_RN=compute_RN(wpd[j][1],wpd[j][2])
            if max<now_RN:
                index=j
                max=now_RN
        result=wpd[index]
        result.append(max)
        wpd.pop(index)
        return result

fuction_pointer={
    0:idle,
    1:FCFS,
    2:SJF,
    3:HRN
}