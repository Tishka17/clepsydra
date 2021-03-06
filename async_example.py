import asyncio
import logging
from datetime import datetime

from clepsydra import create_async_scheduler, SingleRun, Context

scheduler = create_async_scheduler()


@scheduler.task
async def func(context: Context):
    # example of task
    print("Called func with context:", context)
    await asyncio.sleep(5)
    print("func done")


@scheduler.middleware
async def m(context, *args, **kwargs):
    # example of middleware to inject data
    context.data["now"] = datetime.now()
    print("Middleware")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await scheduler.add_job("func", rule=SingleRun(datetime.now()))
    await scheduler.run()


if __name__ == '__main__':
    asyncio.run(main())
