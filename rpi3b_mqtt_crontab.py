from crontab import CronTab

cron = CronTab(user='pi')

job = cron.new(command='python3 rpi3b_mqtt.py', comment='rpi3b_mqtt')
job.minute.every(1)

cron.write()

job.enable()
