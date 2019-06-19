#create by cupcdown
#2019-6-17
#实时作业调度的主函数

import job_scheduling_rt
import GUI_rt
import _thread
import time
import datetime
import random

#界面实体
mygui=GUI_rt.GUI()

#存放待处理作业的list
now_job=[]

#计算当前应当执行的作业
def compute_job():
    while 1:
        show_date=job_scheduling_rt.fuction_pointer[mygui.flag[0]](now_job)
        if show_date==-1:
            pass
        else:
            mygui.update_result(show_date)
            mygui.update_main(now_job)
            time.sleep(show_date[2])

#创造新的作业
def create_job():
    for i in range(2000):
        name="job"+str(i)
        nowTime=datetime.datetime.now().strftime('%H:%M:%S')        #获取当前时间
        n_time=random.randint(1,15)                 #随机生成自习时间
        now_job.append([name,nowTime,n_time])       #将生成的作业放入到now_job的list中
        mygui.update_main(now_job)                  #更新绘制显示等待处理的作业的treeview
        time.sleep(random.randint(1,15))            #线程随机等待一段时间

#主函数
if __name__=='__main__':

    #创建进程
    try:
        _thread.start_new_thread(compute_job)       #计算作业调度顺序线程
        _thread.start_new_thread(create_job)        #生成生产作业线程

    except:
        print("创建进程失败")

    #开始界面主循环
    mygui.start_main_loop()
