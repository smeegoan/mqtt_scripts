# mqtt_scripts
Scripts that publish Hardware Info (Raspberry PI3B. Raspberry PI4 and NUC) into MQTT that can be consumed by Home Assistant

Installation
------------
    pip3 install -r requirements.txt

To schedule the publishing of messages to mqtt server using the xxx_mqtt_crontab.py defaults:

    python3 xxx_mqtt_crontab.py

To confirm the job is scheduled:

    crontab -l




