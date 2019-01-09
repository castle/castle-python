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

    from castle.configuration import configuration

    # Same as setting it through Castle.api_secret
    configuration.api_secret = ':YOUR-API-SECRET'

    # For authenticate method you can set failover strategies: allow(default), deny, challenge, throw
    configuration.failover_strategy = 'deny'

    # Castle::RequestError is raised when timing out in milliseconds (default: 500 milliseconds)
    configuration.request_timeout = 1000

    # Whitelisted and Blacklisted headers are case insensitive and allow to use _ and - as a separator, http prefixes are removed
    # Whitelisted headers
    configuration.whitelisted = ['X_HEADER']
    # or append to default
    configuration.whitelisted = configuration.whitelisted + ['http-x-header']

    # Blacklisted headers take advantage over whitelisted elements
    configuration.blacklisted = ['HTTP-X-header']
    # or append to default
    configuration.blacklisted = configuration.blacklisted + ['X_HEADER']

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

Impersonation mode
------------------

https://castle.io/docs/impersonation


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
