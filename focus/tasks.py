from celery import task
import time


@task
def build_job(p):
    print('ttttttttttime', p, time.asctime())
    return True

# try:
#     print('task start')
#     r = build_job.delay('a')
# except Exception as e:
#     print(e)
