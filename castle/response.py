from castle.exceptions import BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, \
    UserUnauthorizedError, InvalidParametersError, ApiError, InternalServerError


RESPONSE_ERRORS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    419: UserUnauthorizedError,
    422: InvalidParametersError
}


class Response(object):
    def __init__(self, response):
        self.response = response

    def call(self):
        if self.response.text is None or self.response.text == '':
            return {}

        self.verify()

        return self.response.json()

    def verify(self):
        if self.response.status_code >= 200 and self.response.status_code <= 299:
            return

        if self.response.status_code >= 500 and self.response.status_code <= 599:
            raise InternalServerError

        error = RESPONSE_ERRORS.get(self.response.status_code, ApiError)
        raise error(self.response.text)
