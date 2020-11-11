#!/usr/bin/python3

import datetime as dt

from marshmallow import pprint

from marshmallow import Schema, fields, post_load

from marshmallow import ValidationError

class User:
        def __init__(self, name, email, number):
                self.name = name
                self.email = email
                self.created_at = dt.datetime.now()
                self.number = number
        def __repr__(self):
                return "<User(name={self.name!r})>".format(self=self)  +self.email


user=User('ravi', 'rsthakur83@yahoo.com', '100')
#print(user)


class UserSchema(Schema):
        name = fields.Str()
        email = fields.Email()
        created_at = fields.DateTime()
        number = fields.Int()
        sirname = fields.Method("wsrname")        
        def wsrname(self, obj):
            return "THAKUR"

        @post_load
        def make_user(self, data, **kwargs):
            return User(**data)        

user = User(name="Monty", email="monty@python.org", number=100)
schema = UserSchema()
result = schema.dump(user)
print(type(result))
pprint(result)
print("\n")



#user_data = result
#user_data = {'email': 'monty@python.org',
# 'name': 'Monty',
# 'number': 100,
#}
user_data = {'created_at': '2019-07-24T11:43:06.980711+00:00',
 'email': 'monty@python.org',
 'name': 'Monty',
 'number': 100,
 'sirname': 'THAKUR'}
schema = UserSchema()
try:
    deresult = schema.load(user_data, partial=None, unknown=None)
    print("\n")
    print(deresult)
except ValidationError as err:
    err.messages
    valid_data = err.valid_data
    print(err.messages)
    print("\n")
    print("\n")
    print("\n")
    print(valid_data)
