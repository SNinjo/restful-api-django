import json
from time import time, sleep
from django.test import SimpleTestCase
from mongoengine import StringField
from restfulApiDjango.utils import TimestampedDocument

class FakeData(TimestampedDocument):
    name = StringField(required=True)

class TestTimestampedDocument(SimpleTestCase):
    def setUp(self):
        FakeData.drop_collection()

    @classmethod
    def tearDownClass(cls):
        FakeData.drop_collection()

    def test_create_attribute(self):
        FakeData(name='jo').save()
        data = json.loads(FakeData.objects().first().to_json()) # type: ignore
        self.assertTrue('name' in data)

    def test_create_timestamp_when_constructing(self):
        FakeData(name='jo').save()
        data = json.loads(FakeData.objects().first().to_json()) # type: ignore
        self.assertLess(1, time() * 1000 - data['created_at']['$date'])
        self.assertLess(1, time() * 1000 - data['updated_at']['$date'])
        
    def test_update_timestamp_when_saving(self):
        FakeData(name='jo').save()
        sleep(1)
        data = json.loads(FakeData.objects().first().to_json()) # type: ignore
        self.assertLess(1, time() * 1000 - data['updated_at']['$date'])
