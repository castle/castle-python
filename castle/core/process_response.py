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
    419: UserUnauthorizedError,
    422: dict(
        default=InvalidParametersError,
        invalid_request_token=InvalidRequestTokenError,
    ),
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

        error = RESPONSE_ERRORS.get(self.response.status_code, APIError)

        # check if a more specific error is defined for the given type
        if isinstance(error, dict):
            error_type = 'default'

            # attempt to unpack the error type from the response body
            try:
                body = self.response.json()
                if isinstance(body, dict) and 'type' in body:
                    error_type = body['type']
            except JSONDecodeError:
                pass

            error = error[error_type]

        raise error(self.response.text)
