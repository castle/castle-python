## master

## 2.1.1 (2018-02-26)

### Features:
- add reset option to impersonation

## 2.1.0 (2018-02-09)

### Features:
- add support for impersonation

### Breaking Changes:
- switched configuration request_timeout from seconds to milliseconds

## 2.0.0 (2018-02-09)

### Features:
- code reorganization
- added `Client.to_context` method which allows to generate context object from the request
- additional timestamp and sent_at time values are automatically added to the requests
- when data is sent in batches you may want to wrap data options with `Client.to_options` method before you send it to the worker (see README) to include proper timestamp in the query
- added X-Forwarded-For and CF_CONNECTING_IP to whitelisted headers
- fetch IP from CF_CONNECTING_IP if possible

### Breaking Changes:
- Client does not build context object anymore to use previous functionality use `Client.from_request`
- code reorganization

## 1.0.1 (2017-12-08)
* Handle cookies from Django request

## 1.0.0 (2017-10-16)

* Initial release

