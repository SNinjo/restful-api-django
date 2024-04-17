from mongoengine import connect
from mongoengine.connection import disconnect
from restfulApiDjango.settings import *

disconnect('default')
connect(host='mongodb://root:pass@127.0.0.1:27017/test?authSource=admin')
