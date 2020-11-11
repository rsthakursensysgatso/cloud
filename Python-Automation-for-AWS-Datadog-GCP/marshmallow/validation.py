#!/usr/bin/python3.6


from marshmallow import fields, Schema, validates, ValidationError

class Items():
    def __init__(self, items):
        self.items = items

class SimpleListInput(Schema):
    items = fields.List(fields.String(), required=True)

    @validates('items')
    def validate_length(self, value):
        try:
            if len(value) <  3:
                raise ValidationError('Quantity must be greater than 0.')
        except ValidationError as err:
                print(err.messages)
                print('Error')

data = SimpleListInput().load({'items':['ravi', 'thakur']})
#print(data)
