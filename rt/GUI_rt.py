#绘制GUI
#created by cupcdown
#2019-6-10

import tkinter
import tkinter.font as tkFont
from tkinter import ttk
import _thread
import job_scheduling_rt
import time
import datetime
import random

class GUI:

    #初始化函数
    def __init__(self):

        #生成主窗口
        self.windows=tkinter.Tk()       
        self.windows.title('job scheduling')
        self.windows.geometry("800x600")
        self.flag=[0,0]                     #[当前执行的算法是哪个,之前是否是此算法]
        self.rt=[-1,-1]                     #[当前选择的模式,之前的模式]

        #当前等待处理的作业的表格布局
        self.main_frame=tkinter.Frame(self.windows)
        self.mframe_title=tkinter.Label(self.main_frame,
                                        text='等待处理的作业',
                                        font=tkFont.Font(family='song ti', 
                                        size=16))
        self.mframe_title.pack(ipady=20)
        self.tree = ttk.Treeview(self.main_frame,
                                columns=['1','2','3'],
                                height=8,
                                show='headings')
        self.tree.column('1',width=120,anchor='center')
        self.tree.column('2',width=120,anchor='center')
        self.tree.column('3',width=120,anchor='center')
        self.tree.heading('1',text='job name')
        self.tree.heading('2',text='start')
        self.tree.heading('3',text='time')
        self.tree.pack()

        #切换到非实时模式
        def change_to_nrt():
            self.rt[1]=self.rt[0]
            self.rt[0]=0
            

        #切换到实时模式
        def change_to_rt():
            self.rt[1]=self.rt[0]
            self.rt[0]=1

        self.button_rt=tkinter.Button(self.main_frame,
                                    text="实时模式",
                                    command=change_to_rt)
        self.button_nrt=tkinter.Button(self.main_frame,
                                    text="非实时模式",
                                    command=change_to_nrt)
        self.button_nrt.pack(side="left")
        self.button_rt.pack(side="right")

        #显示当前算法的label
        self.label=tkinter.Label(self.main_frame,
                                text="",
                                font=tkFont.Font(family='song ti', size=16))
        self.label.pack(pady=20)
        
        #显示处理结果的表格
        self.result_tree = ttk.Treeview(self.main_frame,
                                        columns=['1','2','3','4'],
                                        height=8,
                                        show='headings')
        self.result_tree.column('1',width=120,anchor='center')
        self.result_tree.column('2',width=120,anchor='center')
        self.result_tree.column('3',width=120,anchor='center')
        self.result_tree.column('4',width=150,anchor='center')
        self.result_tree.heading('1',text='job name')
        self.result_tree.heading('2',text='start')
        self.result_tree.heading('3',text='time')
        self.result_tree.heading('4',text='RN')
        self.result_tree.pack()

        #点击FCFS按钮的响应事件
        def draw_FCFS_result():
            #将flag的类型不为1,或者是工作模式发生改变时
            if not self.flag[0]==1 or (not self.rt[0]==self.rt[1]):     
                self.flag=[1,1]
                self.label["text"]="先来先服务的执行顺序"
                #如果是实时模式下的话，并且之前并没有创建进程，创建工作进程
                if self.rt[0] == 1 and (self.rt[1]==-1 or self.rt[1]==0):
                    create_rt_thread()
                    #并将之前工作模式改为现在的工作模式
                    self.rt[1]=self.rt[0]
                #如果是非实时模式
                elif self.rt[0]==0:
                    #读取文件中的信息，根据选择的算法，显示在界面上
                    main_nrt_thread()

            else:
                self.flag[1]=0
                
        #点击SJF按钮的响应事件
        def draw_SJF_result():
            if not self.flag[0]==2 or (not self.rt[0]==self.rt[1]):
                #将flag变量的类型更改为2,2代表SJF
                self.flag=[2,1]        
                self.label["text"]="最短时间优先的执行顺序"
                #点击按钮时检测之前的工作模式
                if self.rt[0]==1 and (self.rt[1]==-1 or self.rt[1]==0):
                    create_rt_thread()
                    self.rt[1]=self.rt[0]
                elif self.rt[0]==0:
                    main_nrt_thread()
            else:
                self.flag[1]=0

        def draw_HRN_result():
            if not self.flag[0]==3 or (not self.rt[0]==self.rt[1]):
                #将flag变量的类型更改为3,3代表HRN
                self.flag=[3,1]         
                self.label["text"]="响应比优先的执行顺序"
                if self.rt[0]==1 and (self.rt[1]==-1 or self.rt[1]==0):
                    create_rt_thread()
                    self.rt[1]=self.rt[0]
                elif self.rt[0]==0:
                    main_nrt_thread()
            else:
                self.flag[1]=0

        #选择算法的按钮布局
        self.second_frame=tkinter.Frame(self.windows)
        ft=tkFont.Font(family='courier 10 pitch',
                        size=12,
                        weight="bold")                      #设置字体
        label1=tkinter.Label(self.second_frame,text="    ") 
        label2=tkinter.Label(self.second_frame,text="    ")
        self.fcfs_button=tkinter.Button(self.second_frame,  #先来先服务按钮
                                        text="先来先服务",
                                        font=ft,
                                        command=draw_FCFS_result)
        self.fcfs_button.grid(row=0,column=0)
        label1.grid(row=0,column=1)
        self.sjf_button=tkinter.Button(self.second_frame,   #短作业优先按钮
                                        text="短作业优先",
                                        font=ft,
                                        command=draw_SJF_result)
        self.sjf_button.grid(row=0,column=2)
        label2.grid(row=0,column=3)
        self.hnr_button=tkinter.Button(self.second_frame,   #响应比优先按钮
                                        text="响应比优先",
                                        font=ft,
                                        command=draw_HRN_result)
        self.hnr_button.grid(row=0,column=4)
        self.main_frame.pack()
        self.second_frame.pack(pady=10)

    #开始界面主循环
    def start_main_loop(self):
        self.windows.mainloop()
        
    #更新当前的待处理的作业
    def update_main(self,show_date):
        children=self.tree.get_children()
        for i in children:                  #清空之前的treeview的元素
            self.tree.delete(i)
        for i in show_date:
            self.tree.insert('','end',values=i)

    #更新当前正在处理的作业
    def update_result(self,show_date):      #如果上一个算法和当前使用的不同
        if self.flag[1]==1:                 #清空treeview
            children=self.result_tree.get_children()
            for i in children:
                self.result_tree.delete(i)
            self.flag[1]=0
        self.result_tree.insert('',0,values=show_date) #插入当前处理的作业

#界面实体
mygui=GUI()

#存放待处理作业的list,全局变量
global now_job
now_job=[]

#实时状态下计算当前应当执行的作业
def compute_job_rt():
    global now_job
    while mygui.rt[0]==1:
        #通过类似函数指针方式实现动态调用函数
        show_date=job_scheduling_rt.fuction_pointer[mygui.flag[0]](now_job)
        if show_date==-1:
            pass
        else:
            mygui.update_result(show_date)
            mygui.update_main(now_job)
            time.sleep(show_date[2])

#创造新的作业
def create_job():
    i=0
    global now_job
    while mygui.rt[0]==1:
        name="job"+str(i)
        nowTime_before=datetime.datetime.now()      #获取当前时间
        nowTime=nowTime_before.strftime('%H:%M:%S')
        n_time=random.randint(1,15)                 #随机生成自习时间
        now_job.append([name,nowTime,n_time])       #将生成的作业放入到now_job的list中
        mygui.update_main(now_job)                  #更新绘制显示等待处理的作业的treeview
        time.sleep(random.randint(1,15))            #线程随机等待一段时间
        i+=1
    now_job=[]

#生成实时模式下的工作进程
def create_rt_thread():
    try:
        _thread.start_new_thread(create_job)        #生成生产作业线程
        _thread.start_new_thread(compute_job_rt)    #计算作业调度顺序线程
    except:
        print("创建进程失败")

#非实时状态下所要执行的操作
def main_nrt_thread():
    prime_date=job_scheduling_rt.read_date("E:/operating_system/rt/job.csv")
    mygui.update_main(prime_date)
    l=len(prime_date)
    i=0 
    while i <l:
        show_date=job_scheduling_rt.fuction_pointer[mygui.flag[0]](prime_date)
        if not show_date==-1:
            mygui.update_result(show_date)
        i+=1

#主函数
if __name__=='__main__':
    #开始界面主循环
    mygui.start_main_loop()