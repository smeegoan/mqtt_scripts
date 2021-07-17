# MQTT Scripts
Scripts that publish Hardware Info (Raspberry PI3B. Raspberry PI4 and NUC) into MQTT that can be consumed by Home Assistant

Installation
------------
    pip3 install -r requirements.txt

Add your mqtt server address and credentials into config.py

    server = "192.168.1.1"
    user = "user"
    password = "password"

To schedule the publishing of messages to mqtt server using the xxx_mqtt_crontab.py defaults:

    python3 xxx_mqtt_crontab.py

To confirm the job is scheduled:

    crontab -l




