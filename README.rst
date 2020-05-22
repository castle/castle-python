Python SDK for Castle
=====================

.. image:: https://travis-ci.org/castle/castle-python.png
   :alt: Build Status
   :target: https://travis-ci.org/castle/castle-python

`Castle <https://castle.io>`_ **analyzes device, location, and
interaction patterns in your web and mobile apps and lets you stop
account takeover attacks in real-time.**

Installation
------------

``pip install castle``

Configuration
-------------

import and configure the library with your Castle API secret.

.. code:: python

    from castle.configuration import configuration, WHITELISTED

    # Same as setting it through Castle.api_secret
    configuration.api_secret = ':YOUR-API-SECRET'

    # For authenticate method you can set failover strategies: allow(default), deny, challenge, throw
    configuration.failover_strategy = 'deny'

    # Castle::RequestError is raised when timing out in milliseconds (default: 500 milliseconds)
    configuration.request_timeout = 1000

    # Whitelisted and Blacklisted headers are case insensitive and allow to use _ and - as a separator, http prefixes are removed
    # By default all headers are passed, but some are automatically scrubbed.
    # If you need to apply a whitelist, we recommend using the minimum set of
    # standard headers that we've exposed in the `WHITELISTED` constant.
    # Whitelisted headers
    configuration.whitelisted = WHITELISTED + ['X_HEADER']

    # Blacklisted headers take advantage over whitelisted elements. Note that
    # some headers are always scrubbed, for security reasons.
    configuration.blacklisted = ['HTTP-X-header']

    # Castle needs the original IP of the client, not the IP of your proxy or load balancer.
    # The SDK will only trust the proxy chain as defined in the configuration.
    # We try to fetch the client IP based on X-Forwarded-For or Remote-Addr headers in that order,
    # but sometimes the client IP may be stored in a different header or order.
    # The SDK can be configured to look for the client IP address in headers that you specify.
    # If the specified header or X-Forwarded-For default contains a proxy chain with public IP addresses,
    # then one of the following must be set
    # 1. The trusted_proxies value must match the known proxy IP's
    # 2. The trusted_proxy_depth value must be set to the number of known trusted proxies in the chain (see below)
    configuration.ip_headers = []

    # Additionally to make X-Forwarded-For and other headers work better discovering client ip address,
    # and not the address of a reverse proxy server, you can define trusted proxies
    # which will help to fetch proper ip from those headers

    # In order to extract the client IP of the X-Forwarded-For header
    # and not the address of a reverse proxy server, you must define all trusted public proxies
    # you can achieve this by listing all the proxies ip defined by string or regular expressions
    # in trusted_proxies setting
    configuration.trusted_proxies = []
    # or by providing number of trusted proxies used in the chain
    configuration.trusted_proxy_depth = 0

    # If there is no possibility to define options above and there is no other header which can have client ip
    # then you may set trust_proxy_chain = true to trust all of the proxy IP's in X-Forwarded-For
    configuration.trust_proxy_chain = false

    # *Note: default always marked as trusty list is here: Castle::Configuration::TRUSTED_PROXIES

Tracking
--------

Here is a simple example of track event.

.. code:: python

    from castle.client import Client
    from castle import events

    castle = Client.from_request(request)
    castle.track({
      'event': events.LOGIN_SUCCEEDED,
      'user_id': 'user_id'
    })

The client will automatically configure the context for each request.

Signature
---------

.. code:: python

    from secure_mode import signature

    signature(user_id)

will create a signed user_id.

Async tracking
--------------

By default Castle sends requests synchronously. To send requests in a
background worker you can generate data for a worker:

.. code:: python

    from castle.client import Client
    from castle import events

    context = Client.to_context(request)
    options = Client.to_options({
      'event': events.LOGIN_SUCCEEDED,
      'user_id': user.id,
      'properties': {
        'key': 'value'
      },
      'user_traits': {
        'key': 'value'
      }
    })

and use it later in a way

.. code:: python

    from castle.client import Client

    client = Client(context)
    client.track(options)

Events
--------------

List of Recognized Events can be found `here <https://github.com/castle/castle-python/tree/master/castle/events.py>`_ or in the `docs <https://docs.castle.io/api_reference/#list-of-recognized-events>`_.

Impersonation mode
------------------

https://castle.io/docs/impersonation_mode


Exceptions
----------

``CastleError`` will be thrown if the Castle API returns a 400 or a 500
level HTTP response. You can also choose to catch a more `finegrained
error <https://github.com/castle/castle-python/blob/master/castle/exceptions.py>`__.

Documentation
-------------

Documentation and links to additional resources are available at
https://castle.io/docs

.. |Build Status| image:: https://travis-ci.org/castle/castle-python.svg?branch=master
   :target: https://travis-ci.org/castle/castle-python
