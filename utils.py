import time
import tkinter
from tkinter import *
from tkinter import filedialog
import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
from tkinter import messagebox
from scp import SCPClient
import sys


LOG_LINE_NUM=0
def get_current_time():  #获取当前时间
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time

#输出log内容，所有log追加方式写入log文件，限制窗口输出log内容最多8行
def write_log_to_Text(log_data_Text, logmsg):
    global LOG_LINE_NUM
    current_time = get_current_time()
    logmsg_in = str(current_time) + ' ' + str(logmsg) + '\n'
    #日志写入文件
    filetest = open('log.txt', 'a')
    filetest.write(logmsg_in + '\n')
    filetest.close()
    #日志写入窗口
    if LOG_LINE_NUM <= 7:
        log_data_Text.insert(END, logmsg_in)
        log_data_Text.update()
        LOG_LINE_NUM = LOG_LINE_NUM + 1
    else:
        log_data_Text.delete(1.0, 2.0)
        log_data_Text.insert(END, logmsg_in)
        log_data_Text.update()


def get_file_path(MY_GUI):  #获取文件路径并读取文件内容
    filepath = filedialog.askopenfilename()
    try:
        f = open(filepath, encoding='utf-8', errors='ignore')
        if f:
            readlines = f.readlines()
            f.close()
            for line in readlines:
                MY_GUI.init_data_Text.insert(tkinter.INSERT, line)
            return readlines
    except Exception as e:
        write_log_to_Text(MY_GUI.log_data_Text,e)

def check_ip(ipaddr):   #检查ip地址是否合法，合法则返回true，否则弹出提示框
    if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", ipaddr):
        return True
    else:
        messagebox.showinfo('提示', 'IP地址不合法, 请输入正确的IP地址')
        return False
def check_port(port):   #检查端口是否在1-65535范围内，在则返回true，否则弹出提示框
    if re.match(r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]{1}|6553[0-5])$", port):
        return True
    else:
        messagebox.showinfo('提示', '端口不正确，请输入1-65535之间的数字')
        return False


#数据库连接函数，不使用tunnel
def mysql_connect(db_ip, db_name, db_pass,log_data_Text, *sql_cmd):
    # 打开数据库连接,判断数据库连接是否成功
    data = ''
    try:
        db_test = pymysql.connect(db_ip, db_name, db_pass, 'db_flex_sms')
        # 使用cursor()方法获取操作游标
        cursor = db_test.cursor()
        cursor.execute('select version()')
        data = cursor.fetchone()
        db_test.commit()
        # print(data)
        db_test.close()
        data = 'link ok'
        # print(data)
        write_log_to_Text(log_data_Text, '数据库连接成功!')
    except Exception as e:
        write_log_to_Text(log_data_Text, '数据库连接失败!'+str(e))
    if data == 'link ok':
        db = pymysql.connect(db_ip, db_name, db_pass, 'db_flex_sms')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql_value = []
        try:
            for sql in sql_cmd:
                # print(sql)
                cursor.execute(sql)
                sql_value.append(cursor.fetchall())
            return sql_value
        except Exception as e:
            write_log_to_Text(log_data_Text, e)
            # print(sql_value)
        finally:
            db.close()
            return sql_value

#数据库连接函数，使用tunnel
def mysql_tunnel_connet(db_ssh_tunnel_ip,db_ssh_tunnel_logname,db_ssh_tunnel_password,db_ssh_tunnel_port,
            db_ip, db_name, db_pass,log_data_Text,*sql_cmd):
    try:
        with SSHTunnelForwarder(
                (db_ssh_tunnel_ip, db_ssh_tunnel_port),
                ssh_password=db_ssh_tunnel_password,
                ssh_username=db_ssh_tunnel_logname,
                remote_bind_address=(db_ip, 3306)
        ) as tunnel:
            tunnel.start()
            try:
                db_test = pymysql.connect(
                    host='127.0.0.1',
                    port=tunnel.local_bind_port,
                    user=db_name,
                    passwd=db_pass,
                    db='db_flex_sms')
                # 使用cursor()方法获取操作游标
                cursor = db_test.cursor()
                cursor.execute('select version()')
                data = cursor.fetchone()
                db_test.commit()
                # print(data)
                db_test.close()
                data = 'link ok'
                # print(data)
                write_log_to_Text(log_data_Text, '数据库连接成功!')
            except Exception as e:
                write_log_to_Text(log_data_Text, '数据库连接失败!'+str(e))
            if data == 'link ok':
                db = pymysql.connect(
                    host='127.0.0.1',
                    port=tunnel.local_bind_port,
                    user=db_name,
                    passwd=db_pass,
                    db='db_flex_sms'
                )
                # 使用cursor()方法获取操作游标
                cursor = db.cursor()
                try:
                    sql_value = []
                    for sql in sql_cmd:
                        # print(sql)
                        cursor.execute(sql)
                        sql_value.append(cursor.fetchall())
                    return sql_value
                except Exception as e:
                    write_log_to_Text(log_data_Text, e)
                    # print(sql_value)
                finally:
                    db.close()
                    return sql_value
    except Exception as e:
        write_log_to_Text(log_data_Text, e)

#ssh函数，不使用tunnel
def sshlogin(ssh_name, ssh_password, ssh_port, ip,log_data_Text,cmds):
    try:
        ssh = paramiko.SSHClient()  # 创建SSH Client
        ssh.load_system_host_keys()  # 加载系统SSH密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
        ssh.connect(ip, ssh_port, username=ssh_name, password=ssh_password, timeout=5,
                    compress=True)  # SSH连接
        device_result_list = []
        for cmd in cmds:
            # print(cmd)
            stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
            x = stdout.read().decode()  # 读取回显
            stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
            x = stdout.read().decode()  # 读取回显
            device_result_list.append(str(x.strip()))
        ssh.close()
        return device_result_list
    except Exception as e:
        write_log_to_Text(log_data_Text,'%stErrorn %s' % (ip, e))

#ssh函数，使用tunnel
def ssh_tunnel_login(ssh_tunnel_ip, ssh_tunnel_port, ssh_tunnel_logname, ssh_tunnel_password, ssh_name,
                        ssh_password, ssh_port, ip,log_data_Text, cmds):
    try:
        with SSHTunnelForwarder(
                (ssh_tunnel_ip, ssh_tunnel_port),
                ssh_password=ssh_tunnel_password,
                ssh_username=ssh_tunnel_logname,
                remote_bind_address=(ip, ssh_port)
        ) as tunnel:
            tunnel.start()
            ssh = paramiko.SSHClient()  # 创建SSH Client
            ssh.load_system_host_keys()  # 加载系统SSH密钥
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
            ssh.connect('127.0.0.1', tunnel.local_bind_port, username=ssh_name, password=ssh_password,
                        timeout=5, compress=True)
            device_result_list = []
            for cmd in cmds:
                # print(cmd)
                stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
                x = stdout.read().decode()  # 读取回显
                stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
                x = stdout.read().decode()  # 读取回显
                device_result_list.append(str(x.strip()))
        ssh.close()
        return device_result_list
    except Exception as e:
        write_log_to_Text(log_data_Text,e)


def ssh_sftp_put(ip,user,password,port,local_file,remote_file,log_data_Text,remote_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password,timeout=5)
    except Exception as e:
        write_log_to_Text(log_data_Text, e)
    try:
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp.put(local_file, remote_file)
        a = ssh.exec_command("ls %s" %remote_file)
        stdin, stdout, stderr = a
        result=ip+str(stdout.read().decode())+"文件传输完成"
        ssh.close()
        write_log_to_Text(log_data_Text, result)
    except FileNotFoundError as e:
        if "No such file or directory:" in str(e):
            write_log_to_Text(log_data_Text, "本地找不到指定文件" + local_file)
        else:
            write_log_to_Text(log_data_Text, ip+remote_path+"目录不存在")
    except Exception as e:
        write_log_to_Text(log_data_Text, e)
    else:
        write_log_to_Text(log_data_Text, ip+local_file+"文件上传成功")

def ssh_sftp_get(ip,user,password,port,local_file,remote_file,log_data_Text,local_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password,timeout=5)
    except Exception as e:
        write_log_to_Text(log_data_Text, e)
    try:
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp.get(remote_file, local_file)
        a = ssh.exec_command("ls %s" %remote_file)
        stdin, stdout, stderr = a
        result=ip+str(stdout.read().decode())+"文件传输完成"
        ssh.close()
        #write_log_to_Text(log_data_Text, result)
    except FileNotFoundError as e:
        if "No such file or directory:" in str(e):
            write_log_to_Text(log_data_Text,  local_file+"本地找不到指定目录或文件")
        else:
            write_log_to_Text(log_data_Text, ip+remote_file+"远端文件不存在")
    except Exception as e:
        write_log_to_Text(log_data_Text, e)
    else:
        write_log_to_Text(log_data_Text, ip+remote_file+"文件下载成功")






