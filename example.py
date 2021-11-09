from datetime import datetime

from clepsydra import create_scheduler

scheduler = create_scheduler()


@scheduler.task
def func(context):
    pass


scheduler.add_task("func", datetime.now())
scheduler.run()