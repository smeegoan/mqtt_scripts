from crontab import CronTab

cron = CronTab(user='pi')

job = cron.new(command='python3 rpi4_mqtt.py', comment='rpi4_mqtt')
job.minute.every(1)

cron.write()

job.enable()