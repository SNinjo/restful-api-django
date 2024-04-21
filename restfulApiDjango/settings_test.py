import os
from mongoengine import connect
from mongoengine.connection import disconnect
from restfulApiDjango.settings import *

disconnect('default')
connect(host=os.environ.get('MONGO_URI_TEST'))
