from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    BooleanField
)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    message_sent = BooleanField(default=False)