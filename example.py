import logging
from datetime import datetime

from clepsydra import create_scheduler, SingleRun

scheduler = create_scheduler()


@scheduler.task
def func(context):
    print("Called func with context:", context)


logging.basicConfig(level=logging.DEBUG)
scheduler.add_job("func", rule=SingleRun(datetime.now()))
scheduler.run()
