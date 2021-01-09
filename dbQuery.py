import tkinter
from tkinter import *
import utils

db_tunnel_flag=0
def dbQueryWindow(MY_GUI):
    def db_ssh_tunnel():
        global db_tunnel_flag
        db_tunnel_flag = 1
    def free_sql():
        free_sql = db_sql_text.get()
        query_phy_interface('select' + ' ' + free_sql)
    def check_db():  #检查mysql数据库连接是正常
        db_ip = db_ip_text.get()
        db_name = db_logname_text.get()
        db_pass = db_logpasswd_text.get()
        db_port=int(db_port_text.get())
        db_tunnel_ip = db_tunnel_ip_text.get()
        db_tunnel_logname = db_tunnel_logname_text.get()
        db_tunnel_pass=db_tunnel_logpasswd_text.get()
        db_tunnel_port = int(db_tunnel_port_text.get())
        if db_tunnel_flag==0:  #db_tunnel_flag默认值0，若为0则不使用tunnel
            utils.mysql_connect( db_ip, db_name, db_pass,MY_GUI.log_data_Text)
        if db_tunnel_flag==1:   #db_tunnel_flag默认值0，若为1则使用tunnel
            utils.mysql_tunnel_connet(db_tunnel_ip,
                                      db_tunnel_logname,
                                      db_tunnel_pass,
                                      db_tunnel_port,
                                      db_ip,
                                      db_name,
                                      db_pass,
                                      MY_GUI.log_data_Text)

    def query_phy_interface(db_sql):    #物理接口查询函数
        db_ip = db_ip_text.get()
        db_name = db_logname_text.get()
        db_pass = db_logpasswd_text.get()
        db_port = int(db_port_text.get())
        db_tunnel_ip = db_tunnel_ip_text.get()
        db_tunnel_logname = db_tunnel_logname_text.get()
        db_tunnel_pass = db_tunnel_logpasswd_text.get()
        db_tunnel_port = int(db_tunnel_port_text.get())
        if db_tunnel_flag==0:   #db_tunnel_flag默认值0，若为0则不使用tunnel
            interface_query_value=utils.mysql_connect( db_ip, db_name, db_pass,MY_GUI.log_data_Text,db_sql)
        if db_tunnel_flag==1:   #db_tunnel_flag默认值0，若为1则使用tunnel
            interface_query_value=utils.mysql_tunnel_connet(db_tunnel_ip,
                                      db_tunnel_logname,
                                      db_tunnel_pass,
                                      db_tunnel_port,
                                      db_ip,
                                      db_name,
                                      db_pass,
                                      MY_GUI.log_data_Text,
                                      db_sql)
        if interface_query_value:   #判断查询结果是否为空，若不为空则对结果进行处理
            result_value = interface_query_value[0]  # 从查询结果列表中取出第一个值,结果为一个元组
            MY_GUI.result_data_Text.delete(1.0, END)
            for i in range(0, len(result_value)):  # 从设备元组中取出每个设备
                result = ''
                for j in range(0, len(result_value[i])):  # 从每个设备元组中取出每个数值,转换成字符串并进行拼接
                    result = result + str(result_value[i][j]) + ' '
                    j = j + 1
                # print(result)
                MY_GUI.result_data_Text.insert(tkinter.INSERT, result + '\n')  # 输出框输出结果
                MY_GUI.result_data_Text.update()
                i = i + 1
            utils.write_log_to_Text(MY_GUI.log_data_Text,'数据库数据查询完成')  # 打印日志

    def query_wan1_ip(db_sql):
        db_ip = db_ip_text.get()
        db_name = db_logname_text.get()
        db_pass = db_logpasswd_text.get()
        db_port = int(db_port_text.get())
        db_tunnel_ip = db_tunnel_ip_text.get()
        db_tunnel_logname = db_tunnel_logname_text.get()
        db_tunnel_pass = db_tunnel_logpasswd_text.get()
        db_tunnel_port = int(db_tunnel_port_text.get())
        if db_tunnel_flag==0:   #db_tunnel_flag默认值0，若为0则不使用tunnel
            interface_query_value=utils.mysql_connect( db_ip,
                                                       db_name,
                                                       db_pass,
                                                       MY_GUI.log_data_Text,
                                                       db_sql)
        if db_tunnel_flag==1:   #db_tunnel_flag默认值0，若为1则使用tunnel
            interface_query_value=utils.mysql_tunnel_connet(db_tunnel_ip,
                                      db_tunnel_logname,
                                      db_tunnel_pass,
                                      db_tunnel_port,
                                      db_ip,
                                      db_name,
                                      db_pass,
                                      MY_GUI.log_data_Text,
                                      db_sql)
        if interface_query_value:   #判断查询结果是否为空，若不为空则对结果进行处理
            result_value = interface_query_value[0]  # 从查询结果列表中取出第一个值,结果为一个元组
            MY_GUI.result_data_Text.delete(1.0, END)
            for i in range(0, len(result_value)):  # 从设备元组中取出每个设备
                if isinstance(result_value[i][3], str):
                    MY_GUI.init_data_Text.insert(tkinter.INSERT, result_value[i][3] + '\n')  # 数据录入框框输出结果
                    MY_GUI.init_data_Text.update()
                i = i + 1
            utils.write_log_to_Text(MY_GUI.log_data_Text,'数据库数据查询完成')  # 打印日志

    def flexedge_wan1():
        sql_wan1 = "select e.name,e.sn,n.alias,n.ip from gm_eng_netport n Left Join gm_eng e ON e.id =n.engId where n.alias='WAN1'"
        query_phy_interface(sql_wan1)


    def flexedge_wan2():
        sql_wan2 = "select e.name,e.sn,n.alias,n.ip from gm_eng_netport n Left Join gm_eng e ON e.id =n.engId where n.alias='WAN2'"
        query_phy_interface(sql_wan2)

    def flexedge_all_interface():
        all_interface = "select e.name,e.sn ,group_concat( concat_ws( ':', n.alias,n.ip ) order by n.type, n.alias separator ' ' ) from gm_eng e left join gm_eng_netport n ON n.engId= e.id group by e.id"
        query_phy_interface(all_interface)

    def flexedge_wan1ip_to_init_data_Text():
        sql_wan1 = "select e.name,e.sn,n.alias,n.ip from gm_eng_netport n Left Join gm_eng e ON e.id =n.engId where n.alias='WAN1'"
        query_wan1_ip(sql_wan1)

    def flexthinedge_wan1():
        sql_wan1 = "select e.name,e.sn,n.name,n.ip from gm_gateway_netport n Left Join gm_gateway e ON e.id =n.gwId where n.name='WAN1'"
        query_phy_interface(sql_wan1)

    def flexthinedge_wan2():
        sql_wan2 = "select e.name,e.sn,n.name,n.ip from gm_gateway_netport n Left Join gm_gateway e ON e.id =n.gwId where n.name='WAN2'"
        query_phy_interface(sql_wan2)

    def flexthinedge_wan3():
        sql_wan3 = "select e.name,e.sn,n.name,n.ip from gm_gateway_netport n Left Join gm_gateway e ON e.id =n.gwId where n.name='WAN3'"
        query_phy_interface(sql_wan3)

    def flexthinedge_py_all_interface():
        sql_wan3 = "select e.name,e.sn ,group_concat( concat_ws( ':', n.name,n.ip ) order by n.type, n.name separator ' ' ) from gm_gateway e left join gm_gateway_netport n ON n.gwId= e.id group by e.id"
        query_phy_interface(sql_wan3)

    def flexthinedge_wan1ip_to_init_data_Text():
        sql_wan1 = "select e.name,e.sn,n.name,n.ip from gm_gateway_netport n Left Join gm_gateway e ON e.id =n.gwId where n.name='WAN1'"
        query_wan1_ip(sql_wan1)



    init_windown_click = Toplevel()
    check_ip_register = init_windown_click.register(utils.check_ip)
    check_port_register = init_windown_click.register(utils.check_port)
    init_windown_click.title('数据库信息')
    init_windown_click.geometry('450x600')

    db_ip = Label(init_windown_click, text='数据库地址:')
    db_ip.grid(row=0, column=0)
    db_ip_text = StringVar()
    db_ip_text.set('172.19.129.121')
    db_Entry = Entry(init_windown_click, textvariable=db_ip_text,validate='focusout',
                         validatecommand=(check_ip_register, '%P'))
    db_Entry.grid(row=0, column=1)

    db_port = Label(init_windown_click, text='数据库端口:')
    db_port.grid(row=0, column=2)
    db_port_text = StringVar()
    db_port_text.set('3306')
    db_port_Entry = Entry(init_windown_click, textvariable=db_port_text, width=6,validate='focusout',
                         validatecommand=(check_port_register, '%P'))
    db_port_Entry.grid(row=0, column=3)

    db_logname = Label(init_windown_click, text='用户名:')
    db_logname.grid(row=1, column=0)
    db_logname_text = StringVar()
    db_logname_text.set('root')
    db_logname_Entry = Entry(init_windown_click, textvariable=db_logname_text)
    db_logname_Entry.grid(row=1, column=1)

    db_logpasswd = Label(init_windown_click, text='密码:')
    db_logpasswd.grid(row=2, column=0)
    db_logpasswd_text = StringVar()
    db_logpasswd_text.set('Certus@20xx')
    db_logpasswd_Entry = Entry(init_windown_click, textvariable=db_logpasswd_text)
    db_logpasswd_Entry.grid(row=2, column=1)
    # ssh tunnel
    db_ssh_tunnel_ck = Checkbutton(init_windown_click, text='ssh_tunnel', command=db_ssh_tunnel)
    db_ssh_tunnel_ck.grid(row=3, column=0)

    db_tunnel_ip = Label(init_windown_click, text='IP地址:')
    db_tunnel_ip.grid(row=4, column=0)
    db_tunnel_ip_text = StringVar()
    db_tunnel_ip_text.set('172.19.129.121')
    db_tunnel_Entry = Entry(init_windown_click, textvariable=db_tunnel_ip_text,validate='focusout',
                         validatecommand=(check_ip_register, '%P'))
    db_tunnel_Entry.grid(row=4, column=1)

    db_tunnel_port = Label(init_windown_click, text='端口:')
    db_tunnel_port.grid(row=4, column=2)
    db_tunnel_port_text = StringVar()
    db_tunnel_port_text.set('22')
    db_tunnel_port_Entry = Entry(init_windown_click, textvariable=db_tunnel_port_text, width=6,
                                 validate='focusout',validatecommand=(check_port_register, '%P'))
    db_tunnel_port_Entry.grid(row=4, column=3)

    db_tunnel_logname = Label(init_windown_click, text='用户名:')
    db_tunnel_logname.grid(row=5, column=0)
    db_tunnel_logname_text = StringVar()
    db_tunnel_logname_text.set('root')
    db_tunnel_logname_Entry = Entry(init_windown_click, textvariable=db_tunnel_logname_text)
    db_tunnel_logname_Entry.grid(row=5, column=1)

    db_tunnel_logpasswd = Label(init_windown_click, text='密码:')
    db_tunnel_logpasswd.grid(row=6, column=0)
    db_tunnel_logpasswd_text = StringVar()
    db_tunnel_logpasswd_text.set('Certus@20xx')
    db_tunnel_logpasswd_Entry = Entry(init_windown_click, textvariable=db_tunnel_logpasswd_text)
    db_tunnel_logpasswd_Entry.grid(row=6, column=1)
    db_connet_butthon = Button(init_windown_click, text='连接数据库', bg='lightblue', width=10, command=check_db)
    db_connet_butthon.grid(row=7, column=1)

    # FlexEdge 分割线
    db_lab1 = Label(init_windown_click,
                    text='------------------------------------------------------------------------------')
    db_lab1.grid(row=8, column=0, columnspan=5)
    db_lab5 = Label(init_windown_click, text='FlexEdge:')
    db_lab5.grid(row=9, column=0)
    # FlexEdge查询按钮
    db_eng_query_name_wan1_butthon = Button(init_windown_click, text='WAN1', bg='lightblue', width=8,
                                            command=flexedge_wan1)
    db_eng_query_name_wan1_butthon.grid(row=10, column=0)
    db_eng_query_name_wan2_butthon = Button(init_windown_click, text='WAN2', bg='lightblue', width=8,
                                            command=flexedge_wan2)
    db_eng_query_name_wan2_butthon.grid(row=10, column=1)
    db_eng_query_name_allwan_butthon = Button(init_windown_click, text='ALL_PORT', bg='lightblue', width=8,
                                              command=flexedge_all_interface)
    db_eng_query_name_allwan_butthon.grid(row=11, column=0)
    db_eng_WAN1_to_init_data_Text_butthon = Button(init_windown_click, text='WAN1_IP', bg='lightblue', width=8,
                                                   command=flexedge_wan1ip_to_init_data_Text)
    db_eng_WAN1_to_init_data_Text_butthon.grid(row=11, column=1)

    # FlexThinEdge 分割线
    db_lab1 = Label(init_windown_click,
                    text='------------------------------------------------------------------------------')
    db_lab1.grid(row=12, column=0, columnspan=5)
    db_lab5 = Label(init_windown_click, text='FlexThinEdge:')
    db_lab5.grid(row=13, column=0)
    # FlexThinEdge 按钮
    db_gw_query_name_wan1_butthon = Button(init_windown_click, text='WAN1', bg='lightblue', width=8,
                                           command=flexthinedge_wan1)
    db_gw_query_name_wan1_butthon.grid(row=14, column=0)
    db_gw_query_name_wan2_butthon = Button(init_windown_click, text='WAN2', bg='lightblue', width=8,
                                           command=flexthinedge_wan2)
    db_gw_query_name_wan2_butthon.grid(row=14, column=1)
    db_gw_query_name_wan3_butthon = Button(init_windown_click, text='WAN3', bg='lightblue', width=8,
                                           command=flexthinedge_wan3)
    db_gw_query_name_wan3_butthon.grid(row=15, column=0)
    db_gw_query_name_allwan_butthon = Button(init_windown_click, text='ALL_PORT', bg='lightblue', width=8,
                                             command=flexthinedge_py_all_interface)
    db_gw_query_name_allwan_butthon.grid(row=15, column=1)
    db_gw_WAN1_to_init_data_Text_butthon = Button(init_windown_click, text='WAN1_IP', bg='lightblue', width=8,
                                                  command=flexthinedge_wan1ip_to_init_data_Text)
    db_gw_WAN1_to_init_data_Text_butthon.grid(row=14, column=2)

    # 自定义功能分割线
    db_lab1 = Label(init_windown_click,
                    text='------------------------------------------------------------------------------')
    db_lab1.grid(row=16, column=0, columnspan=5)

    db_lab2 = Label(init_windown_click, text='自定义查询:')
    db_lab2.grid(row=17, column=0)
    db_lab3 = Label(init_windown_click, text='select')
    db_lab3.grid(row=18, column=0)

    db_sql_text = StringVar()
    db_sql_text.set('* from gm_eng')
    db_sql_Entry = Entry(init_windown_click, textvariable=db_sql_text, width=45)
    db_sql_Entry.grid(row=18, column=1, columnspan=5)

    db_sql_butthon = Button(init_windown_click, text='查询', bg='lightblue', width=8, command=free_sql)
    db_sql_butthon.grid(row=19, column=0)