import prefect
from prefect import task, Flow
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule


@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello world!")


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(minutes=1),
)

with Flow("hello-flow", schedule=schedule) as flow:
    hello_task()

flow.run()
