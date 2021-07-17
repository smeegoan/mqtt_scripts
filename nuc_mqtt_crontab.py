from crontab import CronTab

cron = CronTab(user='root')

job = cron.new(command='python3 nuc_mqtt.py', comment='nuc_mqtt')
job.minute.every(1)

cron.write()

job.enable()




#    To list all jobs: crontab -l
#    To remove a job from crontab: crontab -u mobman -l | grep -v 'perl /home/mobman/test.pl'  | crontab -u mobman -
#    Remove everything from crontab: crontab -r


