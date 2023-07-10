from mongoengine import Document, StringField, DateTimeField, ReferenceField
from mongoengine.fields import ListField

class Authors(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(max_length=120, required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}

class Quotes(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Authors, required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}
