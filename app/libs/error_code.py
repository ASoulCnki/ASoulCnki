from app.libs.error import APIException


class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0


class CreateSuccess(APIException):
    code = 201
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 0


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden'
