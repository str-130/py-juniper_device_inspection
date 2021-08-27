# -*- coding:UTF-8 -*-

import os
import time
import getpass
import datetime
import subprocess
import string
import re


def eachFile(filepath):
    pathDir = os.listdir(filepath)  
    return pathDir


def create__file(msg):
    o_file_path = "./" + datetime.datetime.now().strftime('%Y年') + '/' + \
        datetime.datetime.now().strftime('%m月%d日') + '/'
    o_full_path = (
        o_file_path + datetime.datetime.now().strftime('%Y-%m-%d') + "巡检" + ".csv")
    o_file = open(o_full_path, "a")
    o_file.write(msg)
    o_file.close()


txt_path = "./" + datetime.datetime.now().strftime('%Y年') + '/' + \
    datetime.datetime.now().strftime('%m月%d日')
path = os.getcwd()
pathDir = os.listdir(txt_path)
print(pathDir)

first_msg = "序号,设备名,系统告警,机框告警,设备SN,设备版本,各组件状态,当前时间,系统启动时间,协议启动时间,最后配置时间,RE当前状态,RE温度,RE CPU温度,RE内存使用率,RE启动时间,RE在线时间\n"
create__file(first_msg)


hostname = b""
now_data = b""
now_fpc = b""
tmp_fpc = b""
msg = b""
now_slot = b""
tmp_slot = b""
uptime_list = [b"",b"",b"",b""]
re_list = [b"",b"",b"",b"",b"",b""]
sys_alarms = b""
cha_alarms = b""
cha_environment = b""
dev_ver = b""
dev_sn = b""



def read_juniper_file(name):
    fopen = open(name, 'r')
    global hostname
    global now_data
    global now_fpc
    global tmp_fpc
    global msg
    global now_slot
    global tmp_slot
    global uptime_list
    global re_list
    global sys_alarms
    global cha_alarms
    global cha_environment
    global dev_ver
    global dev_sn
    global num

    hostname = b""
    now_data = b""
    now_fpc = b""
    tmp_fpc = b""
    msg = b""
    now_slot = b""
    tmp_slot = b""
    uptime_list = [b"",b"",b"",b""]
    re_list = [b"",b"",b"",b"",b"",b""]
    sys_alarms = b""
    cha_alarms = b""
    cha_environment = b""
    dev_ver = b""
    dev_sn = b""
    

    for line in fopen.readlines():
        #line = line.replace("\n","").split(",")
        #print(line)
        
        input_line = line.strip()
        if "show system alarms" in input_line:
            now_data = "show system alarms"
            hostname = re.findall(r"@(.*)>", input_line)
            hostname = str(hostname).replace("[","")
            hostname = str(hostname).replace("\'","")
            hostname = str(hostname).replace("]","")
            print(hostname)
            continue
        
        elif "show chassis alarms" in input_line:
            now_data = "show chassis alarms"
            continue
        elif "show chassis hardware" in input_line:
            now_data = "show chassis hardware"
            continue
        elif "show version" in input_line:
            now_data = "show version"
            continue
        elif "show chassis environment" in input_line:
            now_data = "show chassis environment"
            continue
        elif "show system uptime" in input_line:
            now_data = "show system uptime"
            continue
        elif "show chassis routing-engine" in input_line:
            now_data = "show chassis routing-engine"
            continue

        if  now_data == "show system alarms":
            msg = b""
            if "No alarms"  in input_line:
                sys_alarms = "no alarms" 
            elif "No alarms" not in input_line and "{master" not in input_line and hostname not in input_line:
                sys_alarms = str(sys_alarms) + input_line + '\n'
            elif hostname in input_line:
                now_data = b""                
                sys_alarms = str(sys_alarms).replace("[","")
                sys_alarms = str(sys_alarms).replace("b\'\'","")
                sys_alarms = str(sys_alarms).replace("]","")
                sys_alarms = str(sys_alarms).replace("\'","")
                num += 1
                msg = str(num) + ',' + str(hostname) + ',\"' + str(sys_alarms) +'\",'
                create__file(msg)
        elif  now_data == "show chassis alarms":
            msg = b""

            if "No alarms"  in input_line:
                cha_alarms = "no alarms" 
            elif "No alarms" not in input_line and "{master" not in input_line and hostname not in input_line:
                cha_alarms = str(cha_alarms) + input_line + '\n'
            elif hostname in input_line:
                now_data = b""                
                cha_alarms = str(cha_alarms).replace("[","")
                cha_alarms = str(cha_alarms).replace("b\'\'","")
                cha_alarms = str(cha_alarms).replace("]","")
                cha_alarms = str(cha_alarms).replace("\'","")
                msg = '\"' + str(cha_alarms) +'\",'
                create__file(msg)

        elif now_data == "show chassis hardware":
            msg = b""
            if "Chassis" in input_line  and "Virtual Chassis" not in input_line:
                dev_sn = str(re.findall(r"Chassis\s*(.*)",input_line))
                dev_sn = str(dev_sn).replace("[","")
                dev_sn = str(dev_sn).replace("b\'\'","")
                dev_sn = str(dev_sn).replace("]","")
                dev_sn = str(dev_sn).replace("\'","")
                dev_sn = dev_sn.strip()
                ###正则取完数据后数据会加上"[]",需要删除后才能和后面取到的SN对比
            elif "FPC" in input_line and "FPC CPU" not in input_line and "MX" not in str(hostname):
                if str(dev_sn) in str(re.findall(r"FPC\s..\s*.{1,6}\s*.{1,11}\s*(.*)",input_line)):
                    dev_sn = str(re.findall(r"FPC\s..\s*.{1,6}\s*.{1,11}\s*(.*)",input_line))
                else:
                    dev_sn = str(dev_sn) + "\n" + str(re.findall(r"FPC\s..\s*.{1,6}\s*.{1,11}\s*(.*)",input_line))
            elif (hostname + ">") in input_line:       
                now_data = b""
                dev_sn = str(dev_sn).replace("[","")
                dev_sn = str(dev_sn).replace("b\'\'","")
                dev_sn = str(dev_sn).replace("]","")
                dev_sn = str(dev_sn).replace("\'","")
                dev_sn = dev_sn.strip()
                msg = '\"' + str(dev_sn) +'\",'
                create__file(msg)

        elif now_data == "show version":
            msg = b""
            if "Model" in input_line:
                dev_ver = str(dev_ver) + str(re.findall(r"Model:\s(.*)",input_line))
            elif ("3200" in str(hostname) or "4248" in str(hostname)) and "JUNOS Base OS boot" in input_line:
                dev_ver = str(dev_ver) + " " + str(re.findall(r"JUNOS Base OS boot\s(.*)",input_line)) + "\n"
                
            elif "Junos:" in input_line:
                dev_ver = str(dev_ver) + " " + str(re.findall(r"Junos:\s(.*)",input_line)) + "\n"
            elif (str(hostname) + ">") in input_line:       
                now_data = b""     
                dev_ver = str(dev_ver).replace("[","")
                dev_ver = str(dev_ver).replace("b\'\'","")
                dev_ver = str(dev_ver).replace("]","")
                dev_ver = str(dev_ver).replace("\'","")
                dev_ver = dev_ver.strip()
                msg = '\"' + str(dev_ver) +'\",'
                create__file(msg)


        elif now_data == "show chassis environment" :
            msg = b""

            if "Class Item" in input_line or "OK" in input_line:
                continue
            elif "{master" not in input_line and hostname not in input_line:
                cha_environment = str(cha_environment) + input_line + '\n'
            elif hostname in input_line:
                now_data = b""
                if cha_environment == b"":
                    cha_environment = "OK"
                cha_environment = str(cha_environment).replace("[","")
                cha_environment = str(cha_environment).replace("b\'\'","")
                cha_environment = str(cha_environment).replace("]","")
                cha_environment = str(cha_environment).replace("\'","")
                msg = '\"' + str(cha_environment) +'\",'
                create__file(msg)



        elif  now_data == "show system uptime"  :
            msg = b""
            if ("fpc" in input_line or "localre:" in input_line) and now_fpc == b"":
                now_fpc = input_line.strip()
            elif ("fpc" in input_line or "localre:" in input_line) and now_fpc != b"":
                tmp_fpc = now_fpc
                now_fpc = input_line.strip()
            if tmp_fpc == b"":
                if "Current time:" in input_line:
                    uptime_list[0] =  str(now_fpc) + " " + str(re.findall(r"time:\s*(.*)", input_line))
                if "System booted:" in input_line:
                    uptime_list[1] =  str(now_fpc) + " " + str(re.findall(r"ted:\s*(.*)", input_line))
                if "Protocols started:" in input_line:
                    uptime_list[2] =  str(now_fpc) + " " + str(re.findall(r"ted:\s*(.*)", input_line))
                if "Last configured:" in input_line:
                    uptime_list[3] =  str(now_fpc) + " " + str(re.findall(r"red:\s*(.*)", input_line))
            else:
                if "Current time:" in input_line:
                    uptime_list[0] = uptime_list[0] + '\n' + now_fpc + " " + \
                        str(re.findall(r"time:\s*(.*)", input_line))
                if "System booted:" in input_line:
                    uptime_list[1] = uptime_list[1] + '\n' + now_fpc + " " + \
                        str(re.findall(r"ted:\s*(.*)", input_line))
                if "Protocols started:" in input_line:
                    uptime_list[2] = uptime_list[2] + '\n' + \
                        now_fpc + " " + str(re.findall(r"ted:\s*(.*)", input_line))
                if "Last configured:" in input_line:
                    uptime_list[3] = uptime_list[3] + '\n' + now_fpc + " " + \
                        str(re.findall(r"red:\s*(.*)", input_line))
            if hostname in input_line:
                now_data = b""
                for i in range(0,len(uptime_list)):
                    uptime_list[i] = uptime_list[i].replace("[","")
                    uptime_list[i] = uptime_list[i].replace("b\'\'","")
                    uptime_list[i] = uptime_list[i].replace("]","")
                    uptime_list[i] = uptime_list[i].replace("\'","")
                    uptime_list[i] = uptime_list[i].strip()

                msg = '\"' + str(uptime_list[0]) + '\",\"' + str(uptime_list[1]) + '\",\"' + str(uptime_list[2]) + '\",\"' + str(uptime_list[3]) + '\",' 

                #print (msg)
                create__file(msg)
 
        elif  now_data == "show chassis routing-engine":
            msg = b""
            if "Slot" in input_line  and now_slot == b"":
                now_slot = input_line.strip()
            elif "Slot" in input_line  and now_slot != b"":
                tmp_slot = now_slot
                now_slot = input_line.strip()
            if tmp_slot == b"":
                if "Current state" in input_line:
                    re_list[0] =  str(now_slot) + " " + str(re.findall(r"state\s*(.*)", input_line))
                if "CPU temperature" in input_line:
                    re_list[1] =  str(now_slot) + " " + str(re.findall(r"ture\s*(.*?)\sdeg", input_line)) + " °C"
                if "Temperature" in input_line:
                    re_list[2] =  str(now_slot) + " " + str(re.findall(r"ture\s*(.*?)\sdeg", input_line)) + " °C"
                if "Memory utilization" in input_line:
                    re_list[3] =  str(now_slot) + " " + str(re.findall(r"zation\s*(.*)\sper", input_line)) + "%"
                if "Start time" in input_line:
                    re_list[4] =  str(now_slot) + " " + str(re.findall(r"time\s*(.*)", input_line))
                if "Uptime" in input_line:
                    re_list[5] =  str(now_slot) + " " + str(re.findall(r"time\s*(.*)", input_line))
            else:
                if "Current state" in input_line:
                    re_list[0] = str(re_list[0]) + '\n' + now_slot + " " + str(re.findall(r"state\s*(.*)", input_line))
                if "CPU temperature" in input_line:
                    re_list[1] = str(re_list[1]) + '\n' + now_slot + " " + str(re.findall(r"ture\s*(.*?)\sdeg", input_line)) + " °C"
                if "Temperature" in input_line:
                    re_list[2] = str(re_list[2]) + '\n' + now_slot + " " + str(re.findall(r"ture\s*(.*?)\sdeg", input_line)) + " °C"
                if "Memory utilization" in input_line:
                    re_list[3] = str(re_list[3]) + '\n' + now_slot + " " + str(re.findall(r"zation\s*(.*)\sper", input_line)) + "%"
                if "Start time" in input_line:
                    re_list[4] = str(re_list[4]) + '\n' + now_slot + " " + str(re.findall(r"time\s*(.*)", input_line))
                if "Uptime" in input_line:
                    re_list[5] = str(re_list[5]) + '\n' + now_slot + " " + str(re.findall(r"time\s*(.*)", input_line))

            if hostname in input_line:
                now_data = b""                
                for i in range (0 , len(re_list)):
                    re_list[i] = str(re_list[i]).replace("[","")
                    re_list[i] = str(re_list[i]).replace("b\'\'","")
                    re_list[i] = str(re_list[i]).replace("]","")
                    re_list[i] = str(re_list[i]).replace("\'","")
                    re_list[i] = str(re_list[i]).strip()
                
                #print (re_list)
                msg = '\"' + str(re_list[0]) + '\",\"' + str(re_list[2]) + '\",\"' + str(re_list[1]) + '\",\"' + str(re_list[3]) + '\",\"' + str(re_list[4]) + '\",\"' + str(re_list[5])  +'\"\n' 
                #msg = msg.replace("[","")
                #msg = msg.replace("b\'\'","")
                #msg = msg.replace("]","")
                #msg = msg.replace("\'","")
                #print (msg)
                create__file(msg)


    fopen.close()




num = 0
for allDir in pathDir:
    if "txt" not in allDir:
        continue
    child = txt_path + '\\' + allDir
    read_juniper_file(child)


#raw_input('Press Enter to exit...')
