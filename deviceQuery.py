import tkinter
from tkinter import messagebox, filedialog
from tkinter import *
import os
import utils


ssh_tunnel_flag=0
def_start=1
radio_value=1
def deviceQueryWindow(MY_GUI):
    def ssh_tunnel():   #tunnel是否启用，ssh_tunnel_flag默认值为0，若执行改函数值变为1
        global ssh_tunnel_flag
        ssh_tunnel_flag = 1

    def ping_check(os_cmd): #执行系统命令，ping检测返回检测结果，若通则返回值0，否则返回其他值
        check_result = os.system(os_cmd)
        # print(check_result)
        return check_result

    def device_query_button():      #设备查询按钮函数，不使用tunnel
        ssh_port = int(ssh_port_text.get())
        ssh_name = ssh_logname_text.get()
        ssh_password = ssh_logpasswd_text.get()
        ip_list = MY_GUI.init_data_Text.get(1.0, END).strip().split('\n')   #从页面获取IP地址列表
        # print(ip_list)
        cmd_list = cmd_Text.get(1.0, END).strip().split('\n')   #从页面获取命令列表
        MY_GUI.result_data_Text.delete(1.0, END)    #清空结果输出框
        #检查命令框是否为空，若命令列表为空，则命令列表左右字符串相加也为空
        check_cmd = ''
        for i in range(0, len(cmd_list)):
            check_cmd = check_cmd + cmd_list[i]
            i = i + 1
        for ip in ip_list:          #从地址列表取ip执行查询命令
            global def_start
            if def_start == 1:  #若def_start值为1则执行查询
                if check_cmd:
                    device_result = utils.sshlogin(ssh_name, ssh_password, ssh_port, ip,MY_GUI.log_data_Text,cmd_list)
                else:
                    utils.write_log_to_Text(MY_GUI.log_data_Text, "命令不能为空")
                    break
            elif def_start == 0: #若def_start值为0则终止查询并输出log
                utils.write_log_to_Text(MY_GUI.log_data_Text,"查询运行终止")
                break
            elif def_start == 2:   #若def_start值为2则暂停查询并弹出提示框
                mes = messagebox.askyesno('提示', '是否继续执行')
                if mes is True:     #点击提示框‘YES’，继续执行查询
                    def_start = 1
                else:
                    def_start = 0   #点击提示框‘NO’，停止查询
            result = ''
            if device_result != None:  # 对查询原始结果进行处理，原始数据为列表
                if radio_value == 1:  # 单选框返回值为1则结果逐条输出
                    for i in range(0, len(device_result)):
                        result = str(device_result[i])
                        i = i + 1
                        MY_GUI.result_data_Text.insert(tkinter.INSERT,
                                                       "*" * 20 + ip + "*" * 20 + "\n" + result + '\n' * 2)
                        MY_GUI.result_data_Text.update()
                elif radio_value == 2:  # 单选框返回值为2则结果合并为一条输出
                    for i in range(0, len(device_result)):
                        result = result + str(device_result[i]) + ' '
                        i = i + 1
                    MY_GUI.result_data_Text.insert(tkinter.INSERT, result + '\n')
                    MY_GUI.result_data_Text.update()
                # print(result)
                utils.write_log_to_Text(MY_GUI.log_data_Text, ip + " " + "设备数据查询完成")

    def device_tunnel_query_button():   #设备查询按钮，使用tunnel
        ssh_tunnel_ip = tunnel_ip_text.get()
        ssh_tunnel_port = int(tunnel_port_text.get())
        ssh_tunnel_logname = tunnel_logname_text.get()
        ssh_tunnel_password = tunnel_logpasswd_text.get()
        ssh_port = int(ssh_port_text.get())
        ssh_name = ssh_logname_text.get()
        ssh_password = ssh_logpasswd_text.get()
        ip_list = MY_GUI.init_data_Text.get(1.0, END).strip().split('\n') #从页面获取IP地址列表
        cmd_list = cmd_Text.get(1.0, END).strip().split('\n')   #从页面获取命令列表
        MY_GUI.result_data_Text.delete(1.0, END)    #清空结果输出框
        # 检查命令框是否为空，若命令列表为空，则命令列表左右字符串相加也为空
        check_cmd=''
        for i in range(0,len(cmd_list)):
            check_cmd=check_cmd+cmd_list[i]
            i=i+1
        for ip in ip_list:      #从地址列表取ip执行查询命令
            if def_start == 1:  #若def_start值为1则执行查询
                if check_cmd:    #判断命令列表是否为空，不为空则执行查询
                    device_result = utils.ssh_tunnel_login(ssh_tunnel_ip, ssh_tunnel_port, ssh_tunnel_logname,
                                                 ssh_tunnel_password, ssh_name, ssh_password, ssh_port, ip,
                                                 MY_GUI.log_data_Text, cmd_list)
                else:   #判断命令列表是否为空，为空则输出log，终止查询
                    utils.write_log_to_Text(MY_GUI.log_data_Text,"命令不能为空")
                    break
            elif def_start == 0:    #若def_start值为0则终止查询并输出log
                utils.write_log_to_Text(MY_GUI.log_data_Text,"查询终止")
                break
            elif def_start == 2:    #若def_start值为2则暂停查询并弹出提示框
                mes = messagebox.askyesno('提示', '是否继续执行')
                if mes is True:
                    def_start = 1   #点击提示框‘YES’，继续执行查询
                else:
                    def_start = 0   #点击提示框‘NO’，停止查询
            result = ''
            if device_result != None:   #对查询原始结果进行处理，原始数据为列表
                if radio_value==1:  #单选框返回值为1则结果逐条输出
                    for i in range(0, len(device_result)):
                        result =str(device_result[i])
                        i = i + 1
                        MY_GUI.result_data_Text.insert(tkinter.INSERT,
                                                       "*" * 20 + ip + "*" * 20 + "\n" + result + '\n' * 2)
                        MY_GUI.result_data_Text.update()
                elif radio_value==2:    #单选框返回值为2则结果合并为一条输出
                    for i in range(0, len(device_result)):
                        result = result + str(device_result[i]) + ' '
                        i = i + 1
                    MY_GUI.result_data_Text.insert(tkinter.INSERT, result + '\n')
                    MY_GUI.result_data_Text.update()
                # print(result)
                utils.write_log_to_Text(MY_GUI.log_data_Text,ip + " " + "设备数据查询完成")

    def get_cmdfile_path():     #从本地系统打开文件并获取文件内容
        filepath = filedialog.askopenfilename()
        try:
            f = open(str(filepath), encoding='utf-8', errors='ignore')
            if f:
                readlines = f.readlines()
                f.close()
                for line in readlines:
                    cmd_Text.insert(tkinter.INSERT, line)
                return readlines
        except Exception as e:
            utils.write_log_to_Text(MY_GUI.log_data_Text,e)

    def device_query_start():   #开始查询函数，判断是否需要tunnel，如果需要tunnel则判断tunnel地址是否可达
        global def_start
        global radio_value
        def_start = 1       #执行查询标志，0：停止 1：开始 3：暂停
        ssh_tunnel_ip = tunnel_ip_text.get()    #获取tunnel ip
        os_cmd = 'ping -c 5' + ' ' + ssh_tunnel_ip  #ping 检测命令
        if ssh_tunnel_flag == 1:    #ssh_tunnel_flag 默认为0，不使用tunnel，若tunnel为1则使用tunnel
            tunnel_check_result = ping_check(os_cmd)    #检测tunnel地址是否可达，可达则返回值0，否则为其他值
            if tunnel_check_result == 0:
                device_tunnel_query_button()    #若tunnel地址可达执行该函数
            else:
                utils.write_log_to_Text(MY_GUI.log_data_Text,ssh_tunnel_ip + "地址不可达")
        else:
            device_query_button()

    def stop(): #查询结束函数，执行该函数，def_start值变为0，终止查询
        global def_start
        def_start = 0

    def suspend():  #查询暂停函数，执行该函数，def_start值变为2
        global def_start
        def_start = 2

    r_value = IntVar()  #创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    r_value.set(1)  #默认value为1的单选按钮被选中
    def check_radio():
        global radio_value
        radio_value = r_value.get() #获取单选按钮的值
        #print(radio_value)

    init_windown_device = Toplevel()
    check_ip_register = init_windown_device.register(utils.check_ip)
    check_port_register = init_windown_device.register(utils.check_port)
    init_windown_device.title('设备查询')
    init_windown_device.geometry('450x600')

    # ssh tunnel
    ssh_tunnel_ck = Checkbutton(init_windown_device, text='ssh_tunnel', command=ssh_tunnel)
    ssh_tunnel_ck.grid(row=0, column=0)

    tunnel_ip = Label(init_windown_device, text='IP地址:')
    tunnel_ip.grid(row=1, column=0)
    tunnel_ip_text = StringVar()
    tunnel_ip_text.set('172.19.129.121')
    tunnel_Entry = Entry(init_windown_device, textvariable=tunnel_ip_text, validate='focusout',
                         validatecommand=(check_ip_register, '%P'))
    tunnel_Entry.grid(row=1, column=1)

    tunnel_port = Label(init_windown_device, text='端口:')
    tunnel_port.grid(row=1, column=2)
    tunnel_port_text = StringVar()
    tunnel_port_text.set('22')
    tunnel_port_Entry = Entry(init_windown_device, textvariable=tunnel_port_text, width=6,
                              validate='focusout',validatecommand=(check_port_register, '%P'))
    tunnel_port_Entry.grid(row=1, column=3)

    tunnel_logname = Label(init_windown_device, text='用户名:')
    tunnel_logname.grid(row=2, column=0)
    tunnel_logname_text = StringVar()
    tunnel_logname_text.set('root')
    tunnel_logname_Entry = Entry(init_windown_device, textvariable=tunnel_logname_text)
    tunnel_logname_Entry.grid(row=2, column=1)

    tunnel_logpasswd = Label(init_windown_device, text='密码:')
    tunnel_logpasswd.grid(row=3, column=0)
    tunnel_logpasswd_text = StringVar()
    tunnel_logpasswd_text.set('Certus@20xx')
    tunnel_logpasswd_Entry = Entry(init_windown_device, textvariable=tunnel_logpasswd_text)
    tunnel_logpasswd_Entry.grid(row=3, column=1)

    lab1 = Label(init_windown_device,
                 text='------------------------------------------------------------------------------')
    lab1.grid(row=4, column=0, columnspan=5)

    ssh_lab1 = Label(init_windown_device,
                     text='ssh登录设置')
    ssh_lab1.grid(row=5, column=0)
    ssh_logname = Label(init_windown_device, text='用户名:')
    ssh_logname.grid(row=7, column=0)
    ssh_logname_text = StringVar()
    ssh_logname_text.set('root')
    ssh_logname_Entry = Entry(init_windown_device, textvariable=ssh_logname_text)
    ssh_logname_Entry.grid(row=7, column=1)

    ssh_logpasswd = Label(init_windown_device, text='密码:')
    ssh_logpasswd.grid(row=8, column=0)
    ssh_logpasswd_text = StringVar()
    ssh_logpasswd_text.set('Certus@20xx')
    ssh_logpasswd_Entry = Entry(init_windown_device, textvariable=ssh_logpasswd_text)
    ssh_logpasswd_Entry.grid(row=8, column=1)

    ssh_port = Label(init_windown_device, text='端口:')
    ssh_port.grid(row=8, column=2)
    ssh_port_text = StringVar()
    ssh_port_text.set('22')
    ssh_port_Entry = Entry(init_windown_device, textvariable=ssh_port_text, width=6,
                           validate='focusout',validatecommand=(check_port_register, '%P'))
    ssh_port_Entry.grid(row=8, column=3)
    lab2 = Label(init_windown_device,
                 text='------------------------------------------------------------------------------')
    lab2.grid(row=9, column=0, columnspan=5)
    ipfile_open_butthon = Button(init_windown_device, text='导入IP', bg='lightblue', width=10,
                                 command=lambda:utils.get_file_path(MY_GUI))
    ipfile_open_butthon.grid(row=10, column=0)
    cmdfile_open_butthon = Button(init_windown_device, text='导入命令', bg='lightblue', width=10,
                                  command=get_cmdfile_path)
    cmdfile_open_butthon.grid(row=10, column=1)
    cmdlab = Label(init_windown_device, text='命令列表:')
    cmdlab.grid(row=11, column=0)
    cmd_Text = Text(init_windown_device, width=55, height=6)  # 命令录入框
    cmd_Text.grid(row=12, column=0, rowspan=1, columnspan=7)

    lab3 = Label(init_windown_device,
                 text='------------------------------------------------------------------------------')
    lab3.grid(row=13, column=0, columnspan=5)
    radiolab3 = Label(init_windown_device,text='结果输出格式')
    radiolab3.grid(row=14, column=0, columnspan=1)


    radio1 = Radiobutton(init_windown_device, text="逐条输出", variable=r_value,value=1,command=check_radio)
    radio1.grid(row=14, column=1, columnspan=1)
    radio2 = Radiobutton(init_windown_device, text="合并输出", variable=r_value,value=2,command=check_radio)
    radio2.grid(row=14, column=2, columnspan=1)

    query_butthon = Button(init_windown_device, text='开始查询', bg='lightblue', width=10, command=device_query_start)
    query_butthon.grid(row=15, column=0, columnspan=1)
    query_butthon = Button(init_windown_device, text='结束查询', bg='lightblue', width=10, command=stop)
    query_butthon.grid(row=15, column=2, columnspan=1)
    query_butthon = Button(init_windown_device, text='暂停', bg='lightblue', width=10, command=suspend)
    query_butthon.grid(row=15, column=1, columnspan=1)