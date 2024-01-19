from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, DateField, ListField, ReferenceField

class Author(Document):
    fullname=StringField()
    born_date=DateField()
    born_location=StringField()
    description=StringField()
    quotes=ListField(ReferenceField('Quote'))
    meta={ "collection": "authors" }

class Quote(Document):
    tags=ListField(StringField())
    author=ReferenceField('Author', reverse_delete_rule=CASCADE)
    quote=StringField()
    meta={ "collection": "quotes" }