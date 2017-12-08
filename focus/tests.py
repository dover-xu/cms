import json
from uuid import uuid4
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APIClient
from focus.models import Comment, Praise, MyUser, Note, Tread, Share


class UnitTest(TestCase):
    def setUp(self):
        print('---------setUp')
        # 创建一个用户
        self.user = MyUser.objects.create_user(username=uuid4().hex)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @override_settings(DEBUG=False)
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

    @override_settings(DEBUG=False)
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
            self.assertEqual(len(data) == 5, exceptSuccess)

    @override_settings(DEBUG=False)
    def testApiDetails(self):
        cases = (
            # ('/api/details/', json.dumps({'id': 1, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, False),
            # ('/api/details/', json.dumps({'id': 14, 'current': 1, 'display': 5}), 'application/json;charset=UTF-8', 200, True),
        )
        for path, data, contentType, status, exceptSuccess in cases:
            response = self.client.post(path=path, data=data, content_type=contentType)
            self.assertEqual(response.status_code, status)
            data = response.json()
            print(data)
            self.assertEqual(len(data) == 7, exceptSuccess)

    def tearDown(self):
        print('---------end tearDown')
