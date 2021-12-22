import logging
from datetime import datetime

from clepsydra import create_scheduler, SingleRun, Context

scheduler = create_scheduler()


@scheduler.task
def func(context: Context):
    print("Called func with context:", context)


logging.basicConfig(level=logging.DEBUG)
scheduler.add_job("func", rule=SingleRun(datetime.now()))
scheduler.run()
