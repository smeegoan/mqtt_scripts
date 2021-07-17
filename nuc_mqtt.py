#!/usr/bin/env python3
import config
import paho.mqtt.client as mqtt
import os
import psutil

topicPrefix= "nuc/J4125/"

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('cat /sys/class/thermal/thermal_zone1/temp').readline()
    return str(int(res) / 1000)

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return str(psutil.cpu_percent())

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])


def publish_message(topic, message):
    client = mqtt.Client(client_id="NUC")
    client.username_pw_set(config.user,config.password)
    client.connect(config.server)
    print("Publishing to MQTT topic: " + topic)
    print("Message: " + message)
    client.publish(topic,message, qos=0, retain=False)
    
    
# CPU informatiom
CPU_temp = getCPUtemperature()
CPU_usage = getCPUuse()
publish_message(topicPrefix+"processor_use", CPU_usage)
publish_message(topicPrefix+"temp", CPU_temp)

# RAM information
# Output is in kb, here I convert it in Mb for readability
RAM_stats = getRAMinfo()
RAM_total = round(int(RAM_stats[0]) / 1000,1)
RAM_used = round(int(RAM_stats[1]) / 1000,1)
RAM_free = round(int(RAM_stats[2]) / 1000,1)
RAM_used_percent=str(round(RAM_used*100/RAM_total,2))
publish_message(topicPrefix+"memory_use", RAM_used_percent)

# Disk information
DISK_stats = getDiskSpace()
DISK_total = DISK_stats[0]
DISK_free = DISK_stats[1]
DISK_perc = DISK_stats[3]
publish_message(topicPrefix+"disk_use", DISK_perc[:-1])

