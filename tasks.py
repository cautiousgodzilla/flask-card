from workers import celery
from datetime import datetime
from flask import current_app as app

from celery.schedules import crontab
print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, print_current_time_job.s(), name='add every 10')


@celery.task()
def calculate_aggregate_likes(article_id):
    # You can get all the likes for the `article_id`
    # Calculate the aggregate and store in the DB
    print("#####################################")
    print("Received {}".format(article_id))
    print("#####################################")
    return True

@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print("Hello {}".format(name))


@celery.task()
def print_current_time_job():
    print("START")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string) 
    print("COMPLETE")
