### Intro 
Clepsydra is a mini framework for task scheduling

All parts are designed to be replaceable. 

Main ideas are:
* No pickle! Tasks are stored in readable format, so can be used outside of framework
* Task creator doesn't need to know how tasks are implemented or executed
* Persistence may be implemented
* All workers must follow same async style: be either sync or async functions

Currently project is in the design stage and any APIs are to be changed

### How to use:

Create scheduler (this step will be customizable). 
If your task functions as synchronous, pass param `sync_executor=True`

```python
from clepsydra import create_scheduler

scheduler = create_scheduler() 
```

Register functions that can be scheduled (custom name can be provided for compatibility)

```python
scheduler.task(some_func)
```

Add some job using function name. For example single run:

```python
from clepsydra import SingleRun

job_id = await scheduler.add_job("some_func", rule=SingleRun(when=datetime.now()))
```

Run scheduler:

```python
await scheduler.run()
```