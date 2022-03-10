from json import JSONDecodeError
from castle.errors import BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, \
    UserUnauthorizedError, InvalidParametersError, APIError, InternalServerError, \
    InvalidRequestTokenError
from castle.logger import Logger

RESPONSE_ERRORS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    419: UserUnauthorizedError
}


class CoreProcessResponse(object):
    def __init__(self, response):
        self.response = response

    def call(self):
        if self.response.text is None or self.response.text == '':
            return {}

        self.verify()

        Logger.call("response:", self.response.text)
        return self.response.json()

    def verify(self):
        if self.response.status_code >= 200 and self.response.status_code <= 299:
            return

        if self.response.status_code >= 500 and self.response.status_code <= 599:
            raise InternalServerError

        if self.response.status_code == 422:
            # attempt to unpack the error type from the response body
            try:
                body = self.response.json()
                if isinstance(body, dict) and 'type' in body:
                    if body['type'] == 'invalid_request_token':
                        raise InvalidRequestTokenError(body['message'])
                    raise InvalidParametersError(body['message'])
            except JSONDecodeError:
                raise InvalidParametersError(self.response.text)

        error = RESPONSE_ERRORS.get(self.response.status_code, APIError)
        raise error(self.response.text)
