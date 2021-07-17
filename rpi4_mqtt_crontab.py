from crontab import CronTab

cron = CronTab()

job = cron.new(command='python3 rpi4_mqtt.py', comment='rpi4_mqtt')
job.minute.every(5)

cron.write()

print job.enable()
print job.enable(False)