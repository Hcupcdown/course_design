#绘制GUI
#created by cupcdown
#2019-6-10

import tkinter
import tkinter.font as tkFont
from tkinter import ttk
import _thread

class GUI:

    #初始化函数
    def __init__(self):

        #生成主窗口
        self.windows=tkinter.Tk()       
        self.windows.title('job scheduling')
        self.windows.geometry("800x600")
        self.flag=[0,0]        #存放当前执行的算法是哪个

        #当前等待处理的作业的表格布局
        self.main_frame=tkinter.Frame(self.windows)
        self.mframe_title=tkinter.Label(self.main_frame,text='等待处理的作业',font=tkFont.Font(family='song ti', size=16))   #'courier 10 pitch'
        self.mframe_title.pack(ipady=20)
        self.tree = ttk.Treeview(self.main_frame,columns=['1','2','3'],height=8,show='headings')
        self.tree.column('1',width=120,anchor='center')
        self.tree.column('2',width=120,anchor='center')
        self.tree.column('3',width=120,anchor='center')
        self.tree.heading('1',text='job name')
        self.tree.heading('2',text='start')
        self.tree.heading('3',text='time')
        self.tree.pack()

        #显示当前算法的label
        self.label=tkinter.Label(self.main_frame,text="",font=tkFont.Font(family='song ti', size=16))
        self.label.pack(pady=20)
        
        #显示处理结果的表格
        self.result_tree = ttk.Treeview(self.main_frame,columns=['1','2','3','4'],height=8,show='headings')
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
            if not self.flag[0]==1:     #将flag变量的类型更改为1,1代表FCFS
                self.flag=[1,1]
                self.label["text"]="先来先服务的执行顺序"
            else:
                self.flag[1]=0

        #点击SJF按钮的响应事件
        def draw_SJF_result():
            if not self.flag[0]==2:
                self.flag=[2,1]         #将flag变量的类型更改为2,2代表SJF
                self.label["text"]="最短时间优先的执行顺序"
            else:
                self.flag[1]=0

        def draw_HRN_result():
            if not self.flag[0]==3:
                self.flag=[3,1]         #将flag变量的类型更改为3,3代表HRN
                self.label["text"]="响应比优先的执行顺序"
            else:
                self.flag[1]=0

        #选择算法的按钮布局
        self.second_frame=tkinter.Frame(self.windows)
        ft=tkFont.Font(family='courier 10 pitch', size=12,weight="bold")
        label1=tkinter.Label(self.second_frame,text="    ")
        label2=tkinter.Label(self.second_frame,text="    ")
        self.fcfs_button=tkinter.Button(self.second_frame,text="先来先服务",font=ft,command=draw_FCFS_result)
        self.fcfs_button.grid(row=0,column=0)
        label1.grid(row=0,column=1)
        self.sjf_button=tkinter.Button(self.second_frame,text="短作业优先",font=ft,command=draw_SJF_result)
        self.sjf_button.grid(row=0,column=2)
        label2.grid(row=0,column=3)
        self.hnr_button=tkinter.Button(self.second_frame,text="最高响应比",font=ft,command=draw_HRN_result)
        self.hnr_button.grid(row=0,column=4)
        self.main_frame.pack()
        self.second_frame.pack(pady=10)

    #开始界面主循环
    def start_main_loop(self):
        self.windows.mainloop()
        
    #更新当前的待处理的作业
    def update_main(self,show_date):
        children=self.tree.get_children()
        for i in children:
            self.tree.delete(i)
        for i in show_date:
            self.tree.insert('','end',values=i)

    #更新当前正在处理的作业
    def update_result(self,show_date):
        if self.flag[1]==1:             #如果上一个算法和当前使用的不同，则清空之前的treeview
            children=self.result_tree.get_children()
            for i in children:
                self.result_tree.delete(i)
            self.flag[1]=0
        self.result_tree.insert('',0,values=show_date)      #插入当前处理的作业
