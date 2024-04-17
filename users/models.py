from mongoengine import IntField, StringField
from restfulApiDjango.utils import TimestampedDocument

class User(TimestampedDocument):
    name = StringField(required=True)
    age = IntField(required=True)
