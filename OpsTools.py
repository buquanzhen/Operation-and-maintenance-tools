#_*_ coding: utf-8 _*_
from tkinter import *
from tkinter import filedialog,dialog
import dbQuery,utils, deviceQuery,file_transfer

class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title('OpsTool V1.1')
        # 1068 680 为窗口大小,+10 +10 定义窗口弹出时的默认弹出位置
        self.init_window_name.geometry('1186x650+20+20')
        # 窗口背景色
        self.init_window_name['bg'] = '#FAF0E6'
        # 虚化 值越小虚化程度越高
        #self.init_window_name.attributes('-alpha', 0.9)

        #标签
        self.init_data_lable=Label(self.init_window_name,text='待处理数据')
        self.init_data_lable.grid(row=0,column=0)
        self.result_data_lable=Label(self.init_window_name,text='输出结果')
        self.result_data_lable.grid(row=0,column=12)
        self.log_lable=Label(self.init_window_name,text='日志')
        self.log_lable.grid(row=12,column=0)
        #文本框
        self.init_data_Text=Text(self.init_window_name,width=65,height=25) #原始数据录入框
        self.init_data_Text.grid(row=1,column=0,rowspan=10,columnspan=10)

        self.result_data_Text=Text(self.init_window_name,width=65,height=35) #输出结果输出框
        self.result_data_Text.grid(row=1,column=12,rowspan=15,columnspan=10)

        self.log_data_Text=Text(self.init_window_name,width=65,height=8)    #日志输出框
        self.log_data_Text.grid(row=13,column=0,columnspan=5)
        #滚动条
        self.result_data_scrollbar_y=Scrollbar(self.init_window_name) #创建纵向滚动条
        self.result_data_scrollbar_y.config(command=self.result_data_Text.yview) #将创建的滚动条通过command参数绑定到需要拖动的Text上
        self.result_data_scrollbar_x = Scrollbar(self.init_window_name,orient=HORIZONTAL,wrap=None)  # 创建横向滚动条
        self.result_data_scrollbar_x.config(command=self.result_data_Text.xview)

        self.result_data_Text.config(xscrollcommand=self.result_data_scrollbar_x.set,yscrollcommand=self.result_data_scrollbar_y.set)   #Text反向绑定滚动条
        self.result_data_scrollbar_y.grid(row=1,column=23,rowspan=15,sticky='NS')
        self.result_data_scrollbar_x.grid(row=14, column=12,columnspan=10,sticky='WE')

        #按钮
        #self.open_file=Button(self.init_window_name,text='从文件导入IP',bg='lightblue',width=10,command=lambda:utils.get_file_path(self))
        #self.open_file.grid(row=0,column=1)
        self.output_result=Button(self.init_window_name,text='导出结果',bg='lightblue',width=10,command=self.output_result_file)
        self.output_result.grid(row=0,column=13)
        self.db_button=Button(self.init_window_name, text='数据库查询', bg='lightblue', width=10, command= lambda: dbQuery.dbQueryWindow(self))
        self.db_button.grid(row=1,column=11)
        self.device_query_button=Button(self.init_window_name,text='设备查询',bg='lightblue',width=10,command=lambda:deviceQuery.deviceQueryWindow(self))
        self.device_query_button.grid(row=2,column=11)
        self.up_down_load_button=Button(self.init_window_name,text='文件传输',bg='lightblue',width=10,command=lambda:file_transfer.file_transfer_Window(self))
        self.up_down_load_button.grid(row=3,column=11)


    def output_result_file(self):
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        #print('保存文件：', file_path)
        file_text =self.result_data_Text.get(1.0,END)
        if file_path is not None:
            try:
                with open(file=file_path, mode='w', encoding='utf-8') as file:
                    file.write(file_text)
                self.result_data_Text.delete(1.0,END)
                dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
                                 'strings': ('OK', 'Cancle')})
                utils.write_log_to_Text(self.log_data_Text,'保存完成,文件路径:'+ file_path)
            except Exception as e:
                utils.write_log_to_Text(self.log_data_Text,e)

if __name__ == '__main__':
    def gui_start():
        init_window = Tk()  # 实例化一个父窗口
        ZMJ_PORTAL = MY_GUI(init_window)
        ZMJ_PORTAL.set_init_window()  # 设置根窗口默认属性
        init_window.mainloop()  # 父窗口进入事件循环,可以理解为保持窗口运行,否则界面不展示
    gui_start()
