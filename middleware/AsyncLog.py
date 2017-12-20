from focus.tasks import async_log
import json


class log(object):

    @staticmethod
    def debug(message):
        async_log.delay('debug', message)

    @staticmethod
    def info(message):
        async_log.delay('info', message)

    @staticmethod
    def warn(message):
        async_log.delay('warn', message)

    @staticmethod
    def error(message):
        async_log.delay('error', message)


class AsyncLog(object):

    def process_request(self, request):
        if hasattr(request, 'META'):
            log.info('request->META: ' + str(request.META))

    def process_response(self, request, response):
        log.info('response: ' + str(response))
        return response
