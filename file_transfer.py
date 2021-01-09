import tkinter
from tkinter import messagebox, filedialog
from tkinter import *
import utils
import time
import paramiko
from scp import SCPClient
ssh_tunnel_flag=0
def_start=1
radio_value=1
radio_fileput_down_value=1
current_ip=""
current_device_rate=""
current_file_name=""
current_file_rate=""

def file_transfer_Window(MY_GUI):
    def ssh_tunnel():
        pass

    def get_cmdfile_path():  # 从本地系统打开文件并获取文件内容
        filepath = filedialog.askopenfilename()
        local_flile_Text.insert(tkinter.INSERT,str(filepath)+'\n')
    def get_dir_path():  # 从本地系统打开文件并获取文件内容
         directory = filedialog.askdirectory()
         remote_flilepath_text.set(directory)


    def stop(): #查询结束函数，执行该函数，def_start值变为0，终止查询
        global def_start
        def_start = 0
    def suspend():  #查询暂停函数，执行该函数，def_start值变为2
        global def_start
        def_start = 2

    def progress(filename, size, sent):
        # sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent) / float(size) * 100))
        #v=str(filename.decode()) + "传输进度 %.2f%% " % ((float(sent) / float(size) * 100))
        v1 = int(float(sent) / float(size) * 100)
        file_rate_TexT.delete(1.0, END)
        file_rate_TexT.insert(tkinter.INSERT, str(v1)+"%")
        file_rate_TexT.update()
        if v1==100:
            result=str(current_ip)+" "+str(current_file_name)+"传输进度："+str(v1)+"%"
            MY_GUI.result_data_Text.insert(tkinter.INSERT, result + '\n')
            MY_GUI.result_data_Text.update()




    def ssh_scp_put(ip, user, password, port, local_file, remote_file, log_data_Text, remote_path):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(ip, port, user, password, timeout=5)
            scpclient = SCPClient(ssh_client.get_transport(), progress=progress, socket_timeout=15.0)
        except Exception as e:
            utils.write_log_to_Text(log_data_Text, e)
        try:
            scpclient.put(local_file, remote_file)
            ssh_client.close()
        except FileNotFoundError:
            utils.write_log_to_Text(log_data_Text, "本地找不到指定文件" + local_file)
        except Exception as e:
            if "No such file or directory" in str(e):
                utils.write_log_to_Text(log_data_Text, ip + remote_path + "目录不存在")
            else:
                utils.write_log_to_Text(log_data_Text, e)
        else:
            utils.write_log_to_Text(log_data_Text, ip + local_file + "文件上传成功")

    def ssh_scp_get(ip, user, password, port, local_file, remote_file, log_data_Text, remote_path):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(ip, port, user, password, timeout=5)
            scpclient = SCPClient(ssh_client.get_transport(), progress=progress, socket_timeout=15.0)
        except Exception as e:
            utils.write_log_to_Text(log_data_Text, e)
        try:
            scpclient.get(remote_file, local_file)
            ssh_client.close()
        except FileNotFoundError:
            utils.write_log_to_Text(log_data_Text, "本地找不到指定文件" + local_file)
        except Exception as e:
            if "No such file or directory" in str(e):
                utils.write_log_to_Text(log_data_Text, ip + remote_file + "目录不存在")
            else:
                utils.write_log_to_Text(log_data_Text, e)
        else:
            utils.write_log_to_Text(log_data_Text, ip + remote_file + "文件下载成功")

    def file_trans_put():
        remote_ip_list = MY_GUI.init_data_Text.get(1.0, END).strip().split('\n')    #远端ip 地址列表
        localfile_list = local_flile_Text.get(1.0, END).strip().split('\n')     #待上传文件列表
        ssh_port = int(ssh_port_text.get())
        ssh_name = ssh_logname_text.get()
        ssh_password = ssh_logpasswd_text.get()
        remote_path=remote_flilepath_text.get()
        #本地文件列表文件字符串相加，判断本地文件列表是否为空
        check_localfile_list=''
        for i in range(0, len(localfile_list)):
            check_localfile_list = check_localfile_list + localfile_list[i]
            i = i + 1

        count_ip=0
        for ip in remote_ip_list:  # 从地址列表取ip执行查询命令
            global def_start
            global current_ip
            global current_file_name
            current_ip=ip
            #在窗口输出当前传输设备ip
            device_TexT.delete(1.0, END)
            device_TexT.insert(tkinter.INSERT, ip)
            device_TexT.update()
            lab_device_text = Label(init_windown_device, textvariable=ip)
            lab_device_text.update()
            lab_device_text.grid(sticky=W, row=20, column=1)
            #在窗口输出ip传输进度
            count_ip=count_ip+1
            device_rate= str(count_ip)+"/"+str(len(remote_ip_list))
            device_rate_TexT.delete(1.0, END)
            device_rate_TexT.insert(tkinter.INSERT, str(device_rate))
            device_rate_TexT.update()

            if def_start == 1:  # 若def_start值为1则执行查询
                if check_localfile_list:    #判断本地文件是否为空，不为空则执行
                    for localfile in localfile_list:    #取一个本地文件
                        localfile_dir_list=localfile.split('/') #以“/”分割成列表，取最后一个元素
                        remotefile=remote_path+localfile_dir_list[-1]   #远端目录+本地文件名作为远端文件
                        # 在窗口输出当前传输文件名称
                        current_file_name=localfile_dir_list[-1]
                        file_TexT.delete(1.0, END)
                        file_TexT.insert(tkinter.INSERT,current_file_name)
                        file_TexT.update()

                        if radio_value==1:  #文件传输协议，1为SFTP，2为SCP
                            utils.ssh_sftp_put(ip, ssh_name, ssh_password,ssh_port,localfile,remotefile,
                                               MY_GUI.log_data_Text,remote_path)
                        elif radio_value==2:    #文件传输协议，1为SFTP，2为SCP
                            ssh_scp_put(ip, ssh_name, ssh_password, ssh_port, localfile,remotefile,
                                              MY_GUI.log_data_Text,remote_path)
                else:   #判断本地文件是否为空，为空则输出log
                    utils.write_log_to_Text(MY_GUI.log_data_Text, "本地文件不能为空")
                    break
            elif def_start == 0:  # 若def_start值为0则终止查询并输出log
                utils.write_log_to_Text(MY_GUI.log_data_Text, "文件传输终止")
                break
            elif def_start == 2:  # 若def_start值为2则暂停查询并弹出提示框
                mes = messagebox.askyesno('提示', '是否继续执行')
                if mes is True:  # 点击提示框‘YES’，继续执行查询
                    def_start = 1
                else:
                    def_start = 0  # 点击提示框‘NO’，停止查询

    def file_trans_get():
        remote_ip_list = MY_GUI.init_data_Text.get(1.0, END).strip().split('\n')     #远端ip 地址列表
        remote_file_list = local_flile_Text.get(1.0, END).strip().split('\n')       #待上传文件列表
        ssh_port = int(ssh_port_text.get())
        ssh_name = ssh_logname_text.get()
        ssh_password = ssh_logpasswd_text.get()
        local_path = remote_flilepath_text.get()
        # 远端文件列表文件字符串相加，判断远端文件列表是否为空
        check_remotefile_list = ''
        for i in range(0, len(remote_file_list)):
            check_remotefile_list = check_remotefile_list + remote_file_list[i]
            i = i + 1
        count_ip = 0
        for ip in remote_ip_list:  # 从地址列表取ip执行查询命令
            global def_start
            global current_ip
            global current_file_name
            current_ip=ip
            #在窗口输出当前传输设备ip
            device_TexT.delete(1.0, END)
            device_TexT.insert(tkinter.INSERT, ip)
            device_TexT.update()
            #在窗口输出ip传输进度
            count_ip=count_ip+1
            device_rate= str(count_ip)+"/"+str(len(remote_ip_list))
            device_rate_TexT.delete(1.0, END)
            device_rate_TexT.insert(tkinter.INSERT, str(device_rate))
            device_rate_TexT.update()
            if def_start == 1:  # 若def_start值为1则执行查询
                if check_remotefile_list:   #判断本地文件是否为空，不为空则执行
                    for remotefile in remote_file_list: #取一个本地文件
                        remotelfile_dir_list=remotefile.split('/')  #以“/”分割成列表，取最后一个元素
                        localfile=local_path+ip+"-"+remotelfile_dir_list[-1]     #本地目录+远端文件名作为本地文件
                        # 在窗口输出当前传输文件名称
                        current_file_name = remotelfile_dir_list[-1]
                        file_TexT.delete(1.0, END)
                        file_TexT.insert(tkinter.INSERT, current_file_name)
                        file_TexT.update()
                        if radio_value==1:  #文件传输协议，1为SFTP，2为SCP
                            utils.ssh_sftp_get(ip, ssh_name, ssh_password,ssh_port,localfile,remotefile,
                                               MY_GUI.log_data_Text,local_path)
                        elif radio_value==2:    #文件传输协议，1为SFTP，2为SCP
                            ssh_scp_get(ip, ssh_name, ssh_password, ssh_port, localfile,remotefile,
                                              MY_GUI.log_data_Text,local_path)
                else:
                    utils.write_log_to_Text(MY_GUI.log_data_Text, "远端文件不能为空")
                    break
            elif def_start == 0:  # 若def_start值为0则终止查询并输出log
                utils.write_log_to_Text(MY_GUI.log_data_Text, "文件传输终止")
                break
            elif def_start == 2:  # 若def_start值为2则暂停查询并弹出提示框
                mes = messagebox.askyesno('提示', '是否继续执行')
                if mes is True:  # 点击提示框‘YES’，继续执行查询
                    def_start = 1
                else:
                    def_start = 0  # 点击提示框‘NO’，停止查询


    def file_transfer_start():
        global def_start
        MY_GUI.result_data_Text.delete(1.0, END)  # 清空结果输出框
        def_start = 1  # 执行查询标志，0：停止 1：开始 3：暂停
        if radio_fileput_down_value==1: #判断文件上传或下载，1为文件上传，2为文件下载
            file_trans_put()
        elif radio_fileput_down_value==2:
            file_trans_get()


    r_value = IntVar()  #创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    r_value.set(1)  #默认value为1的单选按钮被选中
    def check_radio():
        global radio_value
        radio_value = r_value.get() #获取单选按钮的值


    r_fileput_down_value = IntVar()  #创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    r_fileput_down_value.set(1)  #默认value为1的单选按钮被选中

    #判断文件上传或下载函数，文件上传和下载页面有调整
    def check_fileput_down_radio():
        global radio_fileput_down_value
        radio_fileput_down_value = r_fileput_down_value.get() #获取单选按钮的值
        #print(radio_fileput_down_value)
        if radio_fileput_down_value==1:
            local_file_butthon = Button(init_windown_device, text='本地文件', bg='lightblue', width=10,
                           command=get_cmdfile_path)
            local_file_butthon.grid(sticky=W,row=12, column=1)
            local_dir_butthon = Button(init_windown_device, text='本地文件路径 ', width=10,state = 'disabled')
            local_dir_butthon.grid(sticky=W,row=15, column=0)
            local_flile_lab = Label(init_windown_device, text='本地文件列表:')
            local_flile_lab.grid(sticky=W,row=13, column=0)
            remote_flilepath_lab = Label(init_windown_device, text='远端文件路径:')
            remote_flilepath_lab.grid(sticky=W,row=15, column=0)
        elif radio_fileput_down_value==2:
            local_file_butthon = Button(init_windown_device, text='本地文件', bg='lightblue', width=10,
                                        command=get_cmdfile_path,state = 'disabled')
            local_file_butthon.grid(sticky=W,row=12, column=1)
            ipfile_open_butthon.grid(sticky=W,row=12, column=0)
            local_flile_lab = Label(init_windown_device, text='远端文件列表:')
            local_flile_lab.grid(sticky=W,row=13, column=0)
            #remote_flilepath_lab = Label(init_windown_device, text='本地文件路径:')
            #remote_flilepath_lab.grid(row=15, column=0)
            local_dir_butthon = Button(init_windown_device, text='本地文件路径', bg='lightblue', width=10,
                                        command=get_dir_path)
            local_dir_butthon.grid(sticky=W,row=15, column=0)

    init_windown_device = Toplevel()
    check_ip_register = init_windown_device.register(utils.check_ip)
    check_port_register = init_windown_device.register(utils.check_port)
    init_windown_device.title('文件传输')
    init_windown_device.geometry('450x600')
    """
    # ssh tunnel
    ssh_tunnel_ck = Checkbutton(init_windown_device, text='ssh_tunnel', command=ssh_tunnel)
    ssh_tunnel_ck.grid(sticky=W,row=0, column=0)

    tunnel_ip = Label(init_windown_device, text='IP地址:')
    tunnel_ip.grid(sticky=W,row=1, column=0)
    tunnel_ip_text = StringVar()
    tunnel_ip_text.set('172.19.129.121')
    tunnel_Entry = Entry(init_windown_device, textvariable=tunnel_ip_text, validate='focusout',
                         validatecommand=(check_ip_register, '%P'))
    tunnel_Entry.grid(sticky=W,row=1, column=1)

    tunnel_port = Label(init_windown_device, text='端口:')
    tunnel_port.grid(sticky=W,row=1, column=2)
    tunnel_port_text = StringVar()
    tunnel_port_text.set('22')
    tunnel_port_Entry = Entry(init_windown_device, textvariable=tunnel_port_text, width=6,
                              validate='focusout', validatecommand=(check_port_register, '%P'))
    tunnel_port_Entry.grid(sticky=W,row=1, column=3)

    tunnel_logname = Label(init_windown_device, text='用户名:')
    tunnel_logname.grid(sticky=W,row=2, column=0)
    tunnel_logname_text = StringVar()
    tunnel_logname_text.set('root')
    tunnel_logname_Entry = Entry(init_windown_device, textvariable=tunnel_logname_text)
    tunnel_logname_Entry.grid(sticky=W,row=2, column=1)

    tunnel_logpasswd = Label(init_windown_device, text='密码:')
    tunnel_logpasswd.grid(sticky=W,row=3, column=0)
    tunnel_logpasswd_text = StringVar()
    tunnel_logpasswd_text.set('Certus@20xx')
    tunnel_logpasswd_Entry = Entry(init_windown_device, textvariable=tunnel_logpasswd_text)
    tunnel_logpasswd_Entry.grid(sticky=W,row=3, column=1)

   # lab1 = Label(init_windown_device,
    #             text='------------------------------------------------------------------------------')
    #lab1.grid(sticky=W,row=4, column=0, columnspan=5)
    """
    ssh_lab1 = Label(init_windown_device,
                     text='ssh登录设置')
    ssh_lab1.grid(sticky=W,row=5, column=0)
    ssh_logname = Label(init_windown_device, text='用户名:')
    ssh_logname.grid(sticky=W,row=7, column=0)
    ssh_logname_text = StringVar()
    ssh_logname_text.set('root')
    ssh_logname_Entry = Entry(init_windown_device, textvariable=ssh_logname_text)
    ssh_logname_Entry.grid(sticky=W,row=7, column=1)

    ssh_logpasswd = Label(init_windown_device, text='密码:')
    ssh_logpasswd.grid(sticky=W,row=8, column=0)
    ssh_logpasswd_text = StringVar()
    ssh_logpasswd_text.set('Certus@20xx')
    ssh_logpasswd_Entry = Entry(init_windown_device, textvariable=ssh_logpasswd_text)
    ssh_logpasswd_Entry.grid(sticky=W,row=8, column=1)

    ssh_port = Label(init_windown_device, text='端口:')
    ssh_port.grid(sticky=W,row=8, column=2)
    ssh_port_text = StringVar()
    ssh_port_text.set('22')
    ssh_port_Entry = Entry(init_windown_device, textvariable=ssh_port_text, width=6,
                           validate='focusout', validatecommand=(check_port_register, '%P'))
    ssh_port_Entry.grid(sticky=W,row=8, column=3)
    lab2 = Label(init_windown_device,
                 text='------------------------------------------------------------------------------')
    lab2.grid(sticky=W,row=9, column=0, columnspan=5)

    ipfile_open_butthon = Button(init_windown_device, text='导入IP', bg='lightblue', width=10,
                                 command=lambda: utils.get_file_path(MY_GUI))
    ipfile_open_butthon.grid(sticky=W,row=12, column=0)
    local_file_butthon = Button(init_windown_device, text='本地文件', bg='lightblue', width=10,
                                command=get_cmdfile_path)
    local_file_butthon.grid(sticky=W,row=12, column=1)
    if radio_fileput_down_value==2:
        local_file_butthon.forget()
        local_file_butthon.grid(sticky=W,row=12, column=1)

    local_flile_lab = Label(init_windown_device, text='本地文件列表：')
    local_flile_lab.grid(sticky=W,row=13, column=0)
    local_flile_Text = Text(init_windown_device, width=53, height=3)  #
    local_flile_Text.grid(sticky=W,row=14, column=0, rowspan=1, columnspan=7)
    
    remote_flilepath_lab = Label(init_windown_device, text='远端文件路径:')
    remote_flilepath_lab.grid(sticky=W,row=15, column=0)

    remote_flilepath_text = StringVar()
    remote_flilepath_text.set('/root/')
    remote_flilepath_Entry = Entry(init_windown_device, textvariable=remote_flilepath_text, width=60)
    remote_flilepath_Entry.grid(sticky=W,row=16, column=0, columnspan=7)

    radio_fileput_down_lab = Label(init_windown_device,text='上传/下载：')
    radio_fileput_down_lab.grid(sticky=W,row=10, column=0, columnspan=1)
    radio_fileput_down_1 = Radiobutton(init_windown_device, text="文件上传", variable=r_fileput_down_value,value=1,command=check_fileput_down_radio)
    radio_fileput_down_1.grid(sticky=W,row=10, column=1, columnspan=1)
    radio_fileput_down_2 = Radiobutton(init_windown_device, text="文件下载", variable=r_fileput_down_value,value=2,command=check_fileput_down_radio)
    radio_fileput_down_2.grid(sticky=W,row=10, column=2, columnspan=1)



    radio_trans_lab = Label(init_windown_device,text='文件传输方式：')
    radio_trans_lab.grid(sticky=W,row=18, column=0, columnspan=1)
    radio_trans_1 = Radiobutton(init_windown_device, text="SFTP", variable=r_value,value=1,command=check_radio)
    radio_trans_1.grid(sticky=W,row=18, column=1, columnspan=1)
    radio_trans_2 = Radiobutton(init_windown_device, text="SCP", variable=r_value,value=2,command=check_radio)
    radio_trans_2.grid(sticky=W,row=18, column=2, columnspan=1)

    lab3 = Label(init_windown_device,
                 text='------------------------------------------------------------------------------')
    lab3.grid(sticky=W,row=19, column=0, columnspan=5)

    lab_device=Label(init_windown_device,text='当前设备IP：')
    lab_device.grid(sticky=W,row=20, column=0, columnspan=1)


    device_TexT = Text(init_windown_device, width=15, height=1)
    device_TexT.grid(sticky=W,row=20, column=1)


    lab_file=Label(init_windown_device,text='当前传输文件：')
    lab_file.grid(sticky=W,row=21, column=0, columnspan=1)
    file_TexT = Text(init_windown_device, width=30, height=1)
    file_TexT.grid(sticky=W,row=21, column=1,columnspan=2)

    lab_file_rate = Label(init_windown_device, text='文件传输进度：')
    lab_file_rate.grid(sticky=W,row=22, column=0, columnspan=1)
    file_rate_TexT = Text(init_windown_device, width=13, height=1)
    file_rate_TexT.grid(sticky=W,row=22, column=1)

    lab_device_rate=Label(init_windown_device,text='设备传输进度：')
    lab_device_rate.grid(sticky=W,row=23, column=0, columnspan=1)
    device_rate_TexT = Text(init_windown_device, width=13, height=1)
    device_rate_TexT.grid(sticky=W,row=23, column=1)


    query_butthon = Button(init_windown_device, text='开始传输', bg='lightblue', width=10, command=file_transfer_start)
    query_butthon.grid(sticky=W,row=24, column=0, columnspan=1)
    query_butthon = Button(init_windown_device, text='结束传输', bg='lightblue', width=10, command=stop)
    query_butthon.grid(sticky=W,row=24, column=2, columnspan=1)
    query_butthon = Button(init_windown_device, text='暂停', bg='lightblue', width=10, command=suspend)
    query_butthon.grid(row=24, column=1, columnspan=1)