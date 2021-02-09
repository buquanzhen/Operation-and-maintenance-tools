import re
import requests
import simplejson as simplejson
import tkinter
from tkinter import *
import utils
from tkinter import messagebox, filedialog
def_start=1
def rttyQueryWindow(MY_GUI):
    def rtty_query(cmd_str,dev_sn):
        ip=rtty_ip_text.get()
        port=rtty_port_text.get()
        rtty_username=rtty_logname_text.get()
        rtty_password=rtty_logpasswd_text.get()
        cmdList = cmd_str.split()
        json_data = {"devid": dev_sn, "username": rtty_username, "password": rtty_password, "cmd": cmdList[0],
                     "params": cmdList[1:]}
        url="http://"+ip+":"+port+"/cmd"
        try:
            r11 = requests.post(url, json=json_data)
            #pattern = re.compile(r'\x1B\[[0-9;]*[a-zA-Z]')
            if len(r11.content) != 0:
                result = r11.content.decode()
                if "+COPS:" in str(result):     #运营商查询，因字典对双引号比较敏感，需要在此对查询结果特殊处理
                    if "7" in str(result):
                        result=str(result).split("+COPS:")[1].split()[0]
                        return result
                    else:
                        return None

                else:
                    resDict = simplejson.loads(result, strict=False)
                    result=resDict['stdout']
                    return result
        except Exception as e:
            #utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn+"不支持"+cmd_str)
            pass
    def dev_model(dev_sn):
        cmd = 'uci show ovslan'
        result = rtty_query(cmd, dev_sn)  # 获取查询原始结果
        #print("model_result=",result)
        try:
            if result != "":
                r1 = result.split('\n')  # 以换行符将原始结果分隔成列表
                r2 = ''
                for i in range(len(r1)):  # 取r1列表包含"dev_model"的元素
                    if "dev_model" in r1[i]:
                        r2 = r1[i]
                r3 = r2.split('\'')  # 以'为分隔符分隔列表r3
                #print("r3=",r3)
                result_out = r3[1]  # 取列表r3第2个元素
                return result_out
        except Exception as e:
            #utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + " 不在线")
            pass
    #从设备network配置文件获取接口角色对应的实际物理接口
    def thin_interface(dev_sn):
        try:
            cmd="cat /etc/config/network"
            result = rtty_query(cmd, dev_sn)  # 获取查询原始结果
            r1 = result.strip().split('\n')
            #print(r1)
            result_list = []
            for i in range(len(r1)): #遍历查询结果的每一个元素，查找包含字符interface和ifname的元素，并加入新的列表
                r2=str(r1[i].strip())   #去掉每一个元素的前后空格
                #print(r2)
                r4=r2.find("interface") #查找包含interface的元素，不包含返回值为-1
                r5=r2.find("ifname")    #查找包含ifname的元素，不包含返回值为-1
                r6=r2.find("pppoe")
                #print("r4=",r4)
                if r4 !=-1:     #如果interface包含在该元素中，则以‘分割，取第二个元素加入新列表
                   r3 = r2.split("\'")
                   #print(r3[1])
                   result_list.append(r3[1])
                   #print(result_list)
                   continue
                if r6 !=-1:
                   r3 = r2.split("\'")
                   # print(r3[1])
                   result_list.append(r3[1])
                   continue
                if r5 !=-1:     #如果ifname包含在该元素中，则以‘分割，取第二个元素加入新列表
                   r3=r2.split("\'")
                   #print(r3[1])
                   result_list.append(r3[1])
                   continue
            #print(result_list)
            return result_list
        except Exception as e:
            utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + " "+str(e))
    #处理查询结果，输出处理后的结果到页面  高新兴模组完全支持，其他模组部分支持
    def data_process(dev_sn,result,identifier,split_flag,out_name):
        if result == "":
            MY_GUI.result_data_Text.insert(tkinter.INSERT, out_name + "\n")  # 输出结果到页面
            MY_GUI.result_data_Text.update()
            MY_GUI.result_data_Text.see(END)
            utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + " " + out_name + " 未查询到")
        elif result == None:
            MY_GUI.result_data_Text.insert(tkinter.INSERT, out_name + "\n")  # 输出结果到页面
            MY_GUI.result_data_Text.update()
            MY_GUI.result_data_Text.see(END)
            utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + " " + out_name + " 未查询到")
        else:
            if identifier in str(result):
                r1 = result.split('\n')  # 以换行符将原始结果分隔成列表
                for i in range(len(r1)):  # 取r1列表包含"dev_model"的元素
                    if identifier in r1[i]:
                        r2 = r1[i]
                        r3 = r2.split(split_flag)  # 以'为分隔符分隔列表r3
                        result_out = r3[1]  # 取列表r3第2个元素
                        MY_GUI.result_data_Text.insert(tkinter.INSERT, out_name + result_out + "\n")  # 输出结果到页面
                        MY_GUI.result_data_Text.update()
                        MY_GUI.result_data_Text.see(END)
                        break
            else:
                MY_GUI.result_data_Text.insert(tkinter.INSERT, out_name + "\n")  # 输出结果到页面
                MY_GUI.result_data_Text.update()
                MY_GUI.result_data_Text.see(END)
                utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + " " + out_name+" 未查询到")
    def flexthinedge_query(dev_sn):
        #设备名称查询
        if name_select.get()==1:
            cmd = "uci show rtty"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "description"
            out_name = "设备名称:"
            split_flag = "\'"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #设备型号查询
        if model_select.get()==1:
            result_out=dev_model(dev_sn)
            MY_GUI.result_data_Text.insert(tkinter.INSERT, "设备型号:" + result_out + "\n")  # 输出结果到页面
            MY_GUI.result_data_Text.update()
            MY_GUI.result_data_Text.see(END)
        #设备版本查询
        if dev_version_select.get() == 1:
            cmd = "uci show ovslan"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "dev_version="
            out_name = "设备版本:"
            split_flag = "\'"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #设备运行模式查询
        if dev_mode_select.get() == 1:
            cmd = "uci show ovslan"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "dev_mode="
            out_name = "运行模式:"
            split_flag = "\'"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #WAN1接口地址查询
        if wan1_select.get()==1:
            port_list=thin_interface(dev_sn)
            for i in range(len(port_list)):
                if port_list[i]=="WAN":
                    if port_list[i+2]=="pppoe":
                       wan_port ="pppoe-WAN"
                    else:
                        wan_port=port_list[i+1]
                    cmd="ifconfig "+wan_port
                    result=rtty_query(cmd,dev_sn)     #获取查询原始结果
                    identifier = "inet addr"
                    out_name = "WAN:"
                    split_flag = ":"
                    data_process(dev_sn, result, identifier, split_flag, out_name)
                    break

        #WAN2接口地址查询
        if wan2_select.get()==1:
            port_list = thin_interface(dev_sn)
            for i in range(len(port_list)):
                if port_list[i] == "WAN2":
                    if port_list[i + 2] == "pppoe":
                        wan_port = "pppoe-WAN"
                    else:
                        wan_port = port_list[i + 1]
                    cmd = "ifconfig " + wan_port
                    result = rtty_query(cmd, dev_sn)  # 获取查询原始结果
                    identifier = "inet addr"
                    out_name = "WAN2:"
                    split_flag = ":"
                    data_process(dev_sn, result, identifier, split_flag, out_name)
                    break

        #WAN3接口地址查询
        if wan3_select.get()==1:
            port_list = thin_interface(dev_sn)
            for i in range(len(port_list)):
                if port_list[i] == "WAN3":
                    if port_list[i + 2] == "pppoe":
                        wan_port = "pppoe-WAN"
                    else:
                        wan_port = port_list[i + 1]
                    cmd = "ifconfig " + wan_port
                    result = rtty_query(cmd, dev_sn)  # 获取查询原始结果
                    identifier = "inet addr"
                    out_name = "WAN3:"
                    split_flag = ":"
                    data_process(dev_sn, result, identifier, split_flag, out_name)
                    break
        #LAN口地址查询
        if lan_select.get()==1:
            cmd = "ifconfig br-LAN"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "inet addr"
            out_name = "LAN:"
            split_flag = ":"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #设备VLAN查询
        if vlan_select.get() == 1:
           cmd = "uci show vlan"
           result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
           identifier = "tag"
           out_name = "VLAN:"
           split_flag = "\'"
           data_process(dev_sn, result, identifier, split_flag, out_name)
        #模组厂商查询
        if lte_Manufacturer_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c ATI"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            if "Quectel" in str(result):    #Quectel模组
                MY_GUI.result_data_Text.insert(tkinter.INSERT, "模组厂商:" + "Quectel" + "\n")  # 输出结果到页面
                MY_GUI.result_data_Text.update()
                MY_GUI.result_data_Text.see(END)
            else:       #高新兴 广和通模组
                identifier = "Manufacturer"
                out_name = "模组厂商:"
                split_flag = ":"
                data_process(dev_sn, result, identifier, split_flag, out_name)
        #模组型号
        if lte_model_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c ATI"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "Model"
            out_name = "模组型号:"
            split_flag = ":"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #模组版本
        if lte_version_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c ATI"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier="Revision"
            out_name="模组版本:"
            split_flag=":"
            data_process(dev_sn,result,identifier,split_flag,out_name)
        #模组IMEI
        if lte_imei_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c ATI"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "IMEI"
            out_name = "模组IMEI:"
            split_flag = ":"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #SIM 是否插卡
        if lte_sim_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c AT+CPIN?"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "+CPIN:"
            out_name = "SIM状态:"
            split_flag = ":"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #SIM 卡号
        if lte_ccid_select.get() == 1:
            cmd1 = "comtool -e -d /dev/ttyUSB2 -c AT+CCID?"
            cmd2 = "comtool -e -d /dev/ttyUSB2 -c AT+ZGETICCID"
            result1 = rtty_query(cmd1,dev_sn)  # 获取查询原始结果
            result2 = rtty_query(cmd2, dev_sn)  # 获取查询原始结果
            if "+CCID:" in str(result1):
                identifier = "+CCID:"
                out_name = "SIM卡号:"
                split_flag = ":"
                data_process(dev_sn, result1, identifier, split_flag, out_name)
            else:
                identifier = "+ZGETICCID:"
                out_name = "SIM卡号:"
                split_flag = ":"
                data_process(dev_sn, result2, identifier, split_flag, out_name)
        #SIM 驻网状态
        if lte_crge_select.get() == 1:
            cmd = "comtool -e -d /dev/ttyUSB2 -c AT+CREG?"
            result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
            identifier = "+CREG:"
            out_name = "驻网状态:"
            split_flag = ":"
            data_process(dev_sn, result, identifier, split_flag, out_name)
        #LTE信号强度查询
        if cqs_select.get() == 1:
           cmd = "comtool -e -d /dev/ttyUSB1 -c AT+CSQ"
           result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
           identifier = "+CSQ:"
           out_name = "信号强度:"
           split_flag = ":"
           data_process(dev_sn, result, identifier, split_flag, out_name)
        #频段
        if lte_zcellinfo_select.get() == 1:
           cmd = "comtool -e -d /dev/ttyUSB2 -c at+zcellinfo?"
           result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
           identifier = "+ZCELLINFO:"
           out_name = "频段:"
           split_flag = ":"
           data_process(dev_sn, result, identifier, split_flag, out_name)
        #运营商
        if lte_operator_select.get() == 1:
           cmd = "comtool -e -d /dev/ttyUSB2 -c at+cops?"
           result = rtty_query(cmd,dev_sn)  # 获取查询原始结果
           if result == "":
               MY_GUI.result_data_Text.insert(tkinter.INSERT, "运营商：" + "\n")  # 输出结果到页面
               MY_GUI.result_data_Text.update()
               MY_GUI.result_data_Text.see(END)
               utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + "运营商：" + " 未查询到")
           elif result == None:
               MY_GUI.result_data_Text.insert(tkinter.INSERT, "运营商：" + "\n")  # 输出结果到页面
               MY_GUI.result_data_Text.update()
               MY_GUI.result_data_Text.see(END)
               utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + "运营商：" + " 未查询到")
           else:
               MY_GUI.result_data_Text.insert(tkinter.INSERT, "运营商：" +result+"\n")  # 输出结果到页面
               MY_GUI.result_data_Text.update()
               MY_GUI.result_data_Text.see(END)
    def date_query():
        global def_start
        dev_sn_list = MY_GUI.init_data_Text.get(1.0, END).strip().split('\n')  # 从页面获取sn列表
        # print(dev_sn_list)
        count_sn = 0
        for dev_sn in dev_sn_list:
            # 在窗口输出当前传输设备ip
            dev_TexT.delete(1.0, END)
            dev_TexT.insert(tkinter.INSERT, dev_sn)
            dev_TexT.update()
            # 在窗口输出ip传输进度
            count_sn = count_sn + 1
            dev_rate = str(count_sn) + "/" + str(len(dev_sn_list))
            dev_rate_TexT.delete(1.0, END)
            dev_rate_TexT.insert(tkinter.INSERT, str(dev_rate))
            dev_rate_TexT.update()
            if def_start==1:    # 若def_start值为1则开始查询
                if dev_sn:      #判断dev_sn 是否为空
                    MY_GUI.result_data_Text.insert(tkinter.INSERT, ("=") * 15 + dev_sn + ("=") * 15 + '\n')  # 输出结果到页面
                    MY_GUI.result_data_Text.update()
                    check = dev_model(dev_sn)  # 通过查询设备类型是返回值是否为None判断是否可达
                    # print(check)
                    if check is not None:
                        flexthinedge_query(dev_sn)
                    else:
                        utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + "不可达！")
                        continue
                else:
                    utils.write_log_to_Text(MY_GUI.log_data_Text, dev_sn + "设备sn不能为空！")
            elif def_start == 0:  # 若def_start值为0则终止查询并输出log
                utils.write_log_to_Text(MY_GUI.log_data_Text, "查询终止")
                break
            elif def_start == 2:  # 若def_start值为2则暂停查询并弹出提示框
                mes = messagebox.askyesno('提示', '是否继续执行')
                if mes is True:  # 点击提示框‘YES’，继续执行查询
                    def_start = 1
                else:
                    def_start = 0  # 点击提示框‘NO’，停止查询
    def query_start():
        global def_start
        def_start = 1  # 执行查询标志，0：停止 1：开始 2：暂停
        date_query()
    def stop(): #查询结束函数，执行该函数，def_start值变为0，终止查询
        global def_start
        def_start = 0
    def suspend():  #查询暂停函数，执行该函数，def_start值变为2
        global def_start
        def_start = 2

    init_windown_rtty = Toplevel()
    init_windown_rtty.title('RTTY设备查询')
    init_windown_rtty.geometry('450x600')
    rtty_config = Label(init_windown_rtty, text='RTTY服务器:')
    rtty_config.grid(sticky=W, row=0, column=0)
    rtty_ip = Label(init_windown_rtty, text='RTTY地址:')
    rtty_ip.grid(sticky=W, row=1, column=0)
    rtty_ip_text = StringVar()
    rtty_ip_text.set('47.101.32.5')
    db_Entry = Entry(init_windown_rtty, textvariable=rtty_ip_text,width=15)
    db_Entry.grid(sticky=W, row=1, column=1)

    rtty_port = Label(init_windown_rtty, text='RTTY端口:')
    rtty_port.grid(sticky=W, row=1, column=2)
    rtty_port_text = StringVar()
    rtty_port_text.set('5916')
    rtty_port_Entry = Entry(init_windown_rtty, textvariable=rtty_port_text, width=6)
    rtty_port_Entry.grid(sticky=W, row=1, column=3)

    rtty_logname = Label(init_windown_rtty, text='用户名:')
    rtty_logname.grid(sticky=W, row=2, column=0)
    rtty_logname_text = StringVar()
    rtty_logname_text.set('root')
    rtty_logname_Entry = Entry(init_windown_rtty, textvariable=rtty_logname_text,width=15)
    rtty_logname_Entry.grid(sticky=W, row=2, column=1)

    rtty_logpasswd = Label(init_windown_rtty, text='密码:')
    rtty_logpasswd.grid(sticky=W, row=3, column=0)
    rtty_logpasswd_text = StringVar()
    rtty_logpasswd_text.set('Certus@20xx')
    rtty_logpasswd_Entry = Entry(init_windown_rtty, textvariable=rtty_logpasswd_text,width=15)
    rtty_logpasswd_Entry.grid(sticky=W, row=3, column=1)

    lab1 = Label(init_windown_rtty,text='-'*80)
    lab1.grid(sticky=W, row=5, column=0, columnspan=5)

    ipfile_open_butthon = Button(init_windown_rtty, text='导入SN', bg='lightblue', width=10,
                                 command=lambda: utils.get_file_path(MY_GUI))
    ipfile_open_butthon.grid(sticky=W, row=6, column=0)

    dev_type = Label(init_windown_rtty, text='FlexThinEdge:')
    dev_type.grid(sticky=W,row=7, column=0)

    dev_info = Label(init_windown_rtty, text='设备信息:')
    dev_info.grid(sticky=W,row=8, column=0)
    #设备名称
    name_select = IntVar()
    device_name = Checkbutton(init_windown_rtty, text='设备名称', variable=name_select,onvalue=1,offvalue=0)
    device_name.grid(sticky=W,row=9, column=0)
    # 设备型号
    model_select = IntVar()
    device_model = Checkbutton(init_windown_rtty, text='设备型号', variable=model_select,onvalue=1,offvalue=0)
    device_model.grid(sticky=W, row=9, column=1)
    # 版本
    dev_version_select = IntVar()
    device_version = Checkbutton(init_windown_rtty, text='设备版本', variable=dev_version_select,onvalue=1,offvalue=0)
    device_version.grid(sticky=W, row=9, column=2)
    # 模式 route模式  bridge模式
    dev_mode_select = IntVar()
    device_mode = Checkbutton(init_windown_rtty, text='运行模式', variable=dev_mode_select,onvalue=1,offvalue=0)
    device_mode.grid(sticky=W, row=9, column=3)

    dev_intface = Label(init_windown_rtty, text='接口:')
    dev_intface.grid(sticky=W,row=11, column=0)
    #设备wan1接口ip
    wan1_select = IntVar()
    device_wan1 = Checkbutton(init_windown_rtty, text='WAN1地址',variable=wan1_select,onvalue=1,offvalue=0)
    device_wan1.grid(sticky=W,row=12, column=0)
    #设备wan2接口ip
    wan2_select = IntVar()
    device_wan2 = Checkbutton(init_windown_rtty, text='WAN2地址', variable=wan2_select,onvalue=1,offvalue=0)
    device_wan2.grid(sticky=W,row=12, column=1)
    #设备LTE接口ip
    wan3_select = IntVar()
    device_wan3 = Checkbutton(init_windown_rtty, text='WAN3地址', variable=wan3_select,onvalue=1,offvalue=0)
    device_wan3.grid(sticky=W,row=12, column=2)
    # 设备LAN口地址
    lan_select = IntVar()
    device_lan = Checkbutton(init_windown_rtty, text='LAN地址', variable=lan_select,onvalue=1,offvalue=0)
    device_lan.grid(sticky=W, row=12, column=3)
    # 设备vlan
    vlan_select = IntVar()
    device_vlan = Checkbutton(init_windown_rtty, text='VLAN', variable=vlan_select,onvalue=1,offvalue=0)
    device_vlan.grid(sticky=W, row=13, column=0)

    dev_lte = Label(init_windown_rtty, text='LTE:')
    dev_lte.grid(sticky=W,row=14, column=0)
    #LTE 模组厂商
    lte_Manufacturer_select = IntVar()
    lte_Manufacturer = Checkbutton(init_windown_rtty, text='模组厂商', variable=lte_Manufacturer_select,onvalue=1,offvalue=0)
    lte_Manufacturer.grid(sticky=W, row=15, column=0)
    #LTE 模组型号
    lte_model_select = IntVar()
    lte_model = Checkbutton(init_windown_rtty, text='模组型号', variable=lte_model_select,onvalue=1,offvalue=0)
    lte_model.grid(sticky=W, row=15, column=1)
    #LTE 版本
    lte_version_select = IntVar()
    lte_version = Checkbutton(init_windown_rtty, text='模组版本', variable=lte_version_select,onvalue=1,offvalue=0)
    lte_version.grid(sticky=W, row=15, column=2)
    #LTE IMEI
    lte_imei_select = IntVar()
    lte_imei = Checkbutton(init_windown_rtty, text='模组IMEI', variable=lte_imei_select,onvalue=1,offvalue=0)
    lte_imei.grid(sticky=W, row=15, column=3)
    # LTE SIM 是否存在
    lte_sim_select = IntVar()
    lte_sim = Checkbutton(init_windown_rtty, text='是否插卡', variable=lte_sim_select,onvalue=1,offvalue=0)
    lte_sim.grid(sticky=W, row=16, column=0)
    # LTE SIM卡号 CCID
    lte_ccid_select = IntVar()
    lte_ccid = Checkbutton(init_windown_rtty, text='SIM卡号', variable=lte_ccid_select,onvalue=1,offvalue=0)
    lte_ccid.grid(sticky=W, row=16, column=1)
    # LTE SIM柱网状态
    lte_crge_select = IntVar()
    lte_crge = Checkbutton(init_windown_rtty, text='驻网状态', variable=lte_crge_select,onvalue=1,offvalue=0)
    lte_crge.grid(sticky=W, row=16, column=2)
    #lte 信号强度
    cqs_select = IntVar()
    device_cqs = Checkbutton(init_windown_rtty, text='信号强度', variable=cqs_select,onvalue=1,offvalue=0)
    device_cqs.grid(sticky=W, row=16, column=3)
    # LTE SIM运营商
    lte_operator_select = IntVar()
    lte_operator = Checkbutton(init_windown_rtty, text='运营商', variable=lte_operator_select,onvalue=1,offvalue=0)
    lte_operator.grid(sticky=W, row=17, column=1)
    # LTE SIM频段
    lte_zcellinfo_select = IntVar()
    lte_zcellinfo = Checkbutton(init_windown_rtty, text='频段', variable=lte_zcellinfo_select,onvalue=1,offvalue=0)
    lte_zcellinfo.grid(sticky=W, row=17, column=0)

    lab2 = Label(init_windown_rtty, text='-' * 80)
    lab2.grid(sticky=W, row=19, column=0, columnspan=5)

    lab_dev = Label(init_windown_rtty, text='当前设备：')
    lab_dev.grid(sticky=W, row=20, column=0, columnspan=1)
    dev_TexT = Text(init_windown_rtty, width=15, height=1)
    dev_TexT.grid(sticky=W, row=20, column=1, columnspan=2)

    lab_dev_rate = Label(init_windown_rtty, text='查询进度：')
    lab_dev_rate.grid(sticky=W, row=21, column=0, columnspan=1)
    dev_rate_TexT = Text(init_windown_rtty, width=15, height=1)
    dev_rate_TexT.grid(sticky=W, row=21, column=1, columnspan=2)

    rtty_start_butthon = Button(init_windown_rtty, text='开始', bg='lightblue', width=8, command=query_start)
    rtty_start_butthon.grid(sticky=W,row=25, column=0)
    rtty_suspend_butthon = Button(init_windown_rtty, text='暂停', bg='lightblue', width=10, command=suspend)
    rtty_suspend_butthon.grid(sticky=W, row=25, column=1, columnspan=1)
    rtty_stop_butthon = Button(init_windown_rtty, text='结束', bg='lightblue', width=10, command=stop)
    rtty_stop_butthon.grid(row=25, column=2, columnspan=1)

    select_dev_infolist=[name_select,model_select,dev_version_select,dev_mode_select]
    select_dev_portlist=[wan1_select,wan2_select,wan3_select,lan_select,vlan_select]
    select_LTE_list=[lte_Manufacturer_select,lte_model_select,lte_version_select,
                 lte_imei_select,lte_sim_select,lte_ccid_select,lte_crge_select,
                 cqs_select,lte_zcellinfo_select,lte_operator_select]

    def select_all(list):
        for i in range(len(list)):
            list[i].set(1)
            #print(select_list[i].get())
    def unselect_all(list):
        for i in range(len(list)):
            list[i].set(0)
            #print(select_list[i].get())
    def thin_select_all():      #所有选项全选
        #select_all(select_alllist)
        dev_info_select_all()
        dev_port_select_all()
        dev_lte_select_all()
    def thin_unselect_all():        #所有选项全不选
        #unselect_all(select_alllist)
        dev_info_unselect_all()
        dev_port_unselect_all()
        dev_lte_unselect_all()
    def dev_info_select_all():      #所有设备信息选项全选
        select_all(select_dev_infolist)
    def dev_info_unselect_all():    #所有设备信息选项全不选
        unselect_all(select_dev_infolist)
    def dev_port_select_all():      #所有设备接口选项全选
        select_all(select_dev_portlist)
    def dev_port_unselect_all():    #所有设备接口选项全不选
        unselect_all(select_dev_portlist)
    def dev_lte_select_all():      #所有lte选项全选
        select_all(select_LTE_list)
    def dev_lte_unselect_all():    #所有lte选项全不选
        unselect_all(select_LTE_list)

    r_thinselect_value = IntVar()  # 创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    # r_fileput_down_value.set(1)  # 默认value为1的单选按钮被选中
    radio_thin_select_all = Radiobutton(init_windown_rtty, text="全选", variable=r_thinselect_value, value=1,
                                       command=thin_select_all)
    radio_thin_select_all.grid(sticky=W, row=7, column=1)
    radio_thin_unselect_all = Radiobutton(init_windown_rtty, text="全不选", variable=r_thinselect_value, value=2,
                                       command=thin_unselect_all)
    radio_thin_unselect_all.grid(sticky=W, row=7, column=2)

    r_dev_info_value = IntVar()  # 创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    radio_dev_info_select_all = Radiobutton(init_windown_rtty, text="全选", variable=r_dev_info_value, value=1,
                                        command=dev_info_select_all)
    radio_dev_info_select_all.grid(sticky=W, row=8, column=1)
    radio_dev_info_unselect_all = Radiobutton(init_windown_rtty, text="全不选", variable=r_dev_info_value, value=2,
                                          command=dev_info_unselect_all)
    radio_dev_info_unselect_all.grid(sticky=W, row=8, column=2)

    r_dev_port_value = IntVar()  # 创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    radio_dev_port_select_all = Radiobutton(init_windown_rtty, text="全选", variable=r_dev_port_value, value=1,
                                            command=dev_port_select_all)
    radio_dev_port_select_all.grid(sticky=W, row=11, column=1)
    radio_dev_port_unselect_all = Radiobutton(init_windown_rtty, text="全不选", variable=r_dev_port_value, value=2,
                                              command=dev_port_unselect_all)
    radio_dev_port_unselect_all.grid(sticky=W, row=11, column=2)

    r_lte_value = IntVar()  # 创建一个Int类型的容器,将单选按钮绑定到同一个容器上
    radio_lte_select_all = Radiobutton(init_windown_rtty, text="全选", variable=r_lte_value, value=1,
                                            command=dev_lte_select_all)
    radio_lte_select_all.grid(sticky=W, row=14, column=1)
    radio_lte_unselect_all = Radiobutton(init_windown_rtty, text="全不选", variable=r_lte_value, value=2,
                                              command=dev_lte_unselect_all)
    radio_lte_unselect_all.grid(sticky=W, row=14, column=2)
