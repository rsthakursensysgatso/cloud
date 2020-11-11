#!/usr/bin/python3

from marshmallow import Schema, fields, post_load, pre_load

from marshmallow import Schema, fields, pre_load


class UserSchema(Schema):
    name = fields.Str()
    slug = fields.Str()

    @pre_load
    def slugify_name(self, in_data, **kwargs):
        in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
        return in_data


schema = UserSchema()
result = schema.load({"name": "Steve", "slug": "Steve Loria "})
result["slug"]  # => 'steve-loria'
print(result["slug"])




####################







class EmployeeSchema(Schema):
    name = fields.Str()
    salary = fields.Int()

    @pre_load
    def increment(self, in_data, **kwargs):
        #in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
#        print(type(in_data["salary"]))
        in_data["salary"]  = in_data["salary"] + 45
        return in_data


schema = EmployeeSchema()
result1 = schema.load({"name": "Steve", "salary": 40})
result1["salary"]  # => 'steve-loria'
print(result1["salary"])
