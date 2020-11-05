master
------

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  `#79 <https://github.com/castle/castle-python/pull/79/files>`__ drop the configuration ``host``, ``port``, ``url_prefix`` options in favor of ``base_url``

4.0.0 (2020-07-06)
------------------

Features:
~~~~~~~~~

-  `#69 <https://github.com/castle/castle-python/pull/69/files>`__ added
   impersonator to properties

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  `#70 <https://github.com/castle/castle-python/pull/70>`__ dropped
   blacklist and whitelist support, in favour of denylist and allowlist

3.3.0 (2020-05-22)
------------------

-  `#67 <https://github.com/castle/castle-python/pull/67>`__ add
   ``trusted_proxy_depth`` and ``trust_proxy_chain`` configuration
   options

3.2.0 (2020-02-31)
------------------

-  `#64 <https://github.com/castle/castle-python/pull/64>`__ dropped
   X-Client-Id from calculation of ip, drop appending default ip headers
   to the ip\_header list config when config is provided (in that case
   default headers have to explicitly provided)

3.1.0 (2020-02-27)
------------------

-  `#61 <https://github.com/castle/castle-python/pull/61>`__ improve
   headers and ip extractions, improve ip\_headers config, add trusted
   proxies config, added more events to events list
-  `#62 <https://github.com/castle/castle-python/pull/62>`__ move
   request,response, session to apis namespace, add config check before
   doing request

3.0.0 (2020-02-13)
------------------

-  `#59 <https://github.com/castle/castle-python/pull/59>`__ drop
   requests min version in ci
-  `#56 <https://github.com/castle/castle-python/pull/56>`__ drop
   special ip header behavior
-  `#58 <https://github.com/castle/castle-python/pull/58>`__ Adds
   ``ip_header`` configuration option

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  `#57 <https://github.com/castle/castle-python/pull/57>`__ dropped
   support for python 2

2.4.0 (2019-11-20)
------------------

-  `#53 <https://github.com/castle/castle-python/pull/53>`__ update
   whitelisting and blacklisting behavior

2.3.1 (2019-04-05)
------------------

-  `#50 <https://github.com/castle/castle-python/pull/50>`__ generate
   new default timestamps for each call

2.3.0 (2019-01-16)
------------------

-  `#48 <https://github.com/castle/castle-python/pull/48>`__ add
   connection pooling
-  `#47 <https://github.com/castle/castle-python/pull/47>`__ add event
   constants
-  `#40 <https://github.com/castle/castle-python/pull/40>`__ remove
   requirement for ``user_id``

2.2.1 (2018-09-04)
------------------

-  `#41 <https://github.com/castle/castle-python/pull/41>`__ add python
   2.6, python 3.7

2.2.0 (2018-04-18)
------------------

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  `#35 <https://github.com/castle/castle-python/pull/35>`__ usage of
   ``traits`` key is deprecated, use ``user_traits`` instead
-  `#38 <https://github.com/castle/castle-python/pull/38>`__ make api
   related errors inherit from ``ApiError``
-  `#38 <https://github.com/castle/castle-python/pull/38>`__ rename
   ``FailoverStrategyValueError`` to ``ConfigurationError``

Enhancements:
~~~~~~~~~~~~~

-  `#37 <https://github.com/castle/castle-python/pull/37>`__
   ``X-Castle-Client-Id`` takes precedence over ``cid`` from ``cookies``
-  `#36 <https://github.com/castle/castle-python/pull/36>`__ raise
   ``ImpersonationFailed`` when impersonation request failed

2.1.1 (2018-02-26)
------------------

Features:
~~~~~~~~~

-  add reset option to impersonation

2.1.0 (2018-02-09)
------------------

Features:
~~~~~~~~~

-  add support for impersonation

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  switched configuration request\_timeout from seconds to milliseconds

2.0.0 (2018-02-09)
------------------

Features:
~~~~~~~~~

-  code reorganization
-  added ``Client.to_context`` method which allows to generate context
   object from the request
-  additional timestamp and sent\_at time values are automatically added
   to the requests
-  when data is sent in batches you may want to wrap data options with
   ``Client.to_options`` method before you send it to the worker (see
   README) to include proper timestamp in the query
-  added X-Forwarded-For and CF\_CONNECTING\_IP to whitelisted headers
-  fetch IP from CF\_CONNECTING\_IP if possible

Breaking Changes:
~~~~~~~~~~~~~~~~~

-  Client does not build context object anymore to use previous
   functionality use ``Client.from_request``
-  code reorganization

1.0.1 (2017-12-08)
------------------

-  Handle cookies from Django request

1.0.0 (2017-10-16)
------------------

-  Initial release
