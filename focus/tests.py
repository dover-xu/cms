import json
from django.test import TestCase


class UnitTest(TestCase):
    def setUp(self):
        pass

    def testApiContents(self):
        cases = (
            ('/api/contents/', json.dumps({'type': 0, 'sort': 0, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 0, 'sort': 1, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 0, 'sort': 2, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 1, 'sort': 0, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 1, 'sort': 1, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 1, 'sort': 2, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 2, 'sort': 0, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 2, 'sort': 1, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/contents/', json.dumps({'type': 2, 'sort': 2, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
        )
        for path, data, contentType, status, exceptSuccess in cases:
            response = self.client.post(path=path, data=data, content_type=contentType)
            self.assertEqual(response.status_code, status)
            data = response.json()
            self.assertEqual(len(data) == 6, exceptSuccess)

    def testApiUcenter(self):
        cases = (
            ('/api/ucenter/', json.dumps({'type': 0, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/ucenter/', json.dumps({'type': 1, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
            ('/api/ucenter/', json.dumps({'type': 2, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
        )
        for path, data, contentType, status, exceptSuccess in cases:
            response = self.client.post(path=path, data=data, content_type=contentType)
            self.assertEqual(response.status_code, status)
            data = response.json()
            self.assertEqual(len(data) == 6, exceptSuccess)

