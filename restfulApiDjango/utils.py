from datetime import datetime, UTC
from mongoengine import Document, DateTimeField

class TimestampedDocument(Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    created_at = DateTimeField(required=True, default=datetime.now(UTC))
    updated_at = DateTimeField(required=True, default=datetime.now(UTC))

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super().save(*args, **kwargs)
