from crontab import CronTab

cron = CronTab()

job = cron.new(command='python3 rpi3b_mqtt.py', comment='rpi3b_mqtt')
job.minute.every(5)

cron.write()

print job.enable()
print job.enable(False)