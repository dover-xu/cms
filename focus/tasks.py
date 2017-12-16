# from celery import task
from cms.celery import app
import logging

logger = logging.getLogger('django')


@app.task
def async_log(tp, message):
    msg = '[focus][view.py]' + message
    if tp == 'debug':
        logger.debug(msg)
    elif tp == 'info':
        logger.info(msg)
    elif tp == 'warn':
        logger.warning(msg)
    elif tp == 'error':
        logger.error(msg)
