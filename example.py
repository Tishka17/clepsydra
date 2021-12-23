import logging
from datetime import datetime

from clepsydra import create_scheduler, SingleRun, Context

scheduler = create_scheduler()


@scheduler.task
def func(context: Context):
    # example of task
    print("Called func with context:", context)


@scheduler.middleware
def m(context, *args, **kwargs):
    # example of middleware to inject data
    context.data["now"] = datetime.now()


def main():
    logging.basicConfig(level=logging.DEBUG)
    scheduler.add_job("func", rule=SingleRun(datetime.now()))
    scheduler.run()


if __name__ == '__main__':
    main()
