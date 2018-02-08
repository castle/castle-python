## master
### Features:
- code reorganization
- added Castle.to_context method which allows to generate context object from the request
- Client has additional timestamp and sent_at time values are automatically added to the requests
- when data is sent in batches you may want to wrap data options with Client.to_options method before you send it to the worker (see README) to include proper timestamp in the query
- added X-Forwarded-For and CF_CONNECTING_IP to whitelisted headers

### Breaking Changes:
- Client does not not build context object anymore to use previous functionality use Castle::Client.from_request

## 1.0.1 (2017-12-08)
* Handle cookies from Django request

## 1.0.0 (2017-10-16)

* Initial release

