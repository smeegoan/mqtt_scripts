#!/usr/bin/env python3
import config
import paho.mqtt.client as mqtt
import os
import psutil
import json

# Return CPU temperature as a character string                                      
def get_pi_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def get_cpu_temperature():
    res = os.popen('cat /sys/class/thermal/thermal_zone1/temp').readline()
    return str(int(res) / 1000)

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def get_ram_info():
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
def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def publish_config(topic, device, sensor, file):
    f = open (file, "r")
    config= json.dumps(json.load(f)).replace("%TOPIC%",topic).replace("%DEVICE%",device).replace("%SENSOR%",sensor)
    publish_message("homeassistant/sensor/"+device+"/"+sensor+"/config", config)

def publish_message(topic, message):
    client = mqtt.Client(client_id="NUC")
    client.username_pw_set(config.user,config.password)
    client.connect(config.server)
    print("Publishing to MQTT topic: " + topic)
    print("Message: " + message)
    client.publish(topic,message, qos=0, retain=False)
    
def publish_all(device, topicPrefix, isPi):    
    publish_config(topicPrefix+"stats/memory/usage", device, "memory", "config/memory.json")
    publish_config(topicPrefix+"stats/disk/usage", device, "disk", "config/disk.json")
    publish_config(topicPrefix+"stats/cpu/usage", device, "cpu", "config/cpu.json")
    publish_config(topicPrefix+"stats/cpu/temperature", device, "temperature", "config/temperature.json")
    
    
    # CPU informatiom
    CPU_temp = get_pi_cpu_temperature() if isPi else get_cpu_temperature()
    CPU_usage = getCPUuse()
    publish_message(topicPrefix+"stats/cpu/usage", CPU_usage)
    publish_message(topicPrefix+"stats/cpu/temperature", CPU_temp)

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = get_ram_info()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    #RAM_free = round(int(RAM_stats[2]) / 1000,1)
    RAM_used_percent=str(round(RAM_used*100/RAM_total,2))
    publish_message(topicPrefix+"stats/memory/usage", RAM_used_percent)

    # Disk information
    DISK_stats = get_disk_space()
    #DISK_total = DISK_stats[0]
    #DISK_free = DISK_stats[1]
    DISK_perc = DISK_stats[3]
    publish_message(topicPrefix+"stats/disk/usage", DISK_perc[:-1])

