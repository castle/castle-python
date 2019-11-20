## master

## 2.3.2 (2019-11-20)

- [#53](https://github.com/castle/castle-python/pull/53) Update whitelisting and blacklisting behavior

## 2.3.1 (2019-04-05)

- [#50](https://github.com/castle/castle-python/pull/50) generate new default timestamps for each call

## 2.3.0 (2019-01-16)

- [#48](https://github.com/castle/castle-python/pull/48) add connection pooling
- [#47](https://github.com/castle/castle-python/pull/47) add event constants
- [#40](https://github.com/castle/castle-python/pull/40) remove requirement for `user_id`

## 2.2.1 (2018-09-04)

- [#41](https://github.com/castle/castle-python/pull/41) add python 2.6, python 3.7

## 2.2.0 (2018-04-18)

### Breaking Changes:

- [#35](https://github.com/castle/castle-python/pull/35) usage of `traits` key is deprecated, use `user_traits` instead
- [#38](https://github.com/castle/castle-python/pull/38) make api related errors inherit from `ApiError`
- [#38](https://github.com/castle/castle-python/pull/38) rename `FailoverStrategyValueError` to `ConfigurationError`

### Enhancements:

- [#37](https://github.com/castle/castle-python/pull/37) `X-Castle-Client-Id` takes precedence over `cid` from `cookies`
- [#36](https://github.com/castle/castle-python/pull/36) raise `ImpersonationFailed` when impersonation request failed

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

