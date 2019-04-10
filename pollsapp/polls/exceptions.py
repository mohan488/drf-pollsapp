# python
from __future__ import unicode_literals

# libs
from rest_framework import exceptions, status
from rest_framework.views import exception_handler


class ServiceValidationError(Exception):

    def __init__(self, error_code=None):
        self.error_code = error_code


class APIExceptionBase(exceptions.APIException):

    def __init__(self, error_code=None, request=None, *args, **kwargs):
        super(APIExceptionBase, self).__init__(*args, **kwargs)
        self.error_code = error_code
        self.request = request


class Http400(APIExceptionBase):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = u'Bad request.'

    def __init__(self, errors=None, *args, **kwargs):
        super(Http400, self).__init__(*args, **kwargs)
        self.errors = errors


class Http403(APIExceptionBase):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = u'You do not have permission to perform this action.'


class Http404(APIExceptionBase):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = u'Not Found.'


class Http409(APIExceptionBase):
    status_code = status.HTTP_409_CONFLICT
    default_detail = u'Conflict.'


class Http503(APIExceptionBase):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = u'Service unavailable.'

