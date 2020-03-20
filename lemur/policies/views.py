from flask import Blueprint
from flask_restful import reqparse, Api

from lemur.policies import service
from lemur.auth.service import AuthenticatedResource
from lemur.auth.permissions import SensitiveDomainPermission

from lemur.common.schema import validate_schema
from lemur.common.utils import paginated_parser

from lemur.policies.schemas import (
    polices_input_schema,
    polices_output_schema,
    policess_output_schema
)

mod = Blueprint("polices", __name__)
api = Api(mod)


class PolicesList(AuthenticatedResource):
    """ Defines the 'domains' endpoint """

    def __init__(self):
        super(PolicesList, self).__init__()

    @validate_schema(None, policess_output_schema)
    def get(self):
        """
        .. http:get:: /domains

           The current domain list

           **Example request**:

           .. sourcecode:: http

              GET /domains HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript

              {
                "items": [
                    {
                      "id": 1,
                      "name": "www.example.com",
                      "sensitive": false
                    },
                    {
                      "id": 2,
                      "name": "www.example2.com",
                      "sensitive": false
                    }
                  ]
                "total": 2
              }

           :query sortBy: field to sort on
           :query sortDir: asc or desc
           :query page: int default is 1
           :query filter: key value pair format is k;v
           :query count: count number. default is 10
           :reqheader Authorization: OAuth token to authenticate
           :statuscode 200: no error
           :statuscode 403: unauthenticated
        """
        parser = paginated_parser.copy()
        args = parser.parse_args()
        return service.render(args)

    @validate_schema(polices_input_schema, polices_output_schema)
    def post(self, data=None):
        print(data["name"], data["days"])
        """
        .. http:post:: /domains

           The current domain list

           **Example request**:

           .. sourcecode:: http

              GET /domains HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

              {
                "name": "www.example.com",
                "sensitive": false
              }

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript

              {
                "id": 1,
                "name": "www.example.com",
                "sensitive": false
              }

           :query sortBy: field to sort on
           :query sortDir: asc or desc
           :query page: int default is 1
           :query filter: key value pair format is k;v
           :query count: count number default is 10
           :reqheader Authorization: OAuth token to authenticate
           :statuscode 200: no error
           :statuscode 403: unauthenticated
        """
        return service.create(name=data["name"], days=data["days"])

class Police(AuthenticatedResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Police, self).__init__()

    @validate_schema(None, polices_output_schema)
    def get(self, police_id):
        """
        .. http:get:: /sources/1

           Get a specific account

           **Example request**:

           .. sourcecode:: http

              GET /sources/1 HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript

              {
                "options": [
                    {
                        "name": "accountNumber",
                        "required": true,
                        "value": 111111111112,
                        "helpMessage": "Must be a valid AWS account number!",
                        "validation": "/^[0-9]{12,12}$/",
                        "type": "int"
                    }
                ],
                "pluginName": "aws-source",
                "id": 3,
                "lastRun": "2015-08-01T15:40:58",
                "description": "test",
                "label": "test"
              }

           :reqheader Authorization: OAuth token to authenticate
           :statuscode 200: no error
        """
        return service.get(police_id)

    @validate_schema(polices_input_schema, polices_output_schema)
    def put(self, police_id, data=None):
        """
        .. http:put:: /sources/1

           Updates an account

           **Example request**:

           .. sourcecode:: http

              POST /sources/1 HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

              {
                "options": [
                    {
                        "name": "accountNumber",
                        "required": true,
                        "value": 111111111112,
                        "helpMessage": "Must be a valid AWS account number!",
                        "validation": "/^[0-9]{12,12}$/",
                        "type": "int"
                    }
                ],
                "pluginName": "aws-source",
                "id": 3,
                "lastRun": "2015-08-01T15:40:58",
                "description": "test",
                "label": "test"
              }

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript

              {
                "options": [
                    {
                        "name": "accountNumber",
                        "required": true,
                        "value": 111111111112,
                        "helpMessage": "Must be a valid AWS account number!",
                        "validation": "/^[0-9]{12,12}$/",
                        "type": "int"
                    }
                ],
                "pluginName": "aws-source",
                "id": 3,
                "lastRun": "2015-08-01T15:40:58",
                "description": "test",
                "label": "test"
              }

           :arg accountNumber: aws account number
           :arg label: human readable account label
           :arg description: some description about the account
           :reqheader Authorization: OAuth token to authenticate
           :statuscode 200: no error
        """
        return service.update(
            police_id,
            name=data["name"],
            days=data["days"],
        )

    def delete(self, police_id):
        service.delete(police_id)
        return {"result": True}


api.add_resource(PolicesList, "/polices", endpoint="polices")
api.add_resource(Police, "/polices/<int:police_id>", endpoint="police")
