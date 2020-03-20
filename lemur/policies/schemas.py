"""
.. module: lemur.policies.schemas
    :platform: unix
    :copyright: (c) 2018 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from marshmallow import fields

from lemur.common.schema import LemurOutputSchema, LemurInputSchema


class RotationPolicyOutputSchema(LemurOutputSchema):
    id = fields.Integer()
    name = fields.String()
    days = fields.Integer()


class RotationPolicyNestedOutputSchema(RotationPolicyOutputSchema):
    pass


class RotationPolicyInputSchema(LemurInputSchema):
    id = fields.Integer()
    name = fields.String(required=True)
    days = fields.Integer(required=True)


polices_input_schema = RotationPolicyInputSchema()
polices_output_schema = RotationPolicyOutputSchema()
policess_output_schema = RotationPolicyOutputSchema(many=True)
