Python SDK for Castle
=====================

.. image:: https://github.com/castle/castle-python/actions/workflows/specs.yml/badge.svg?branch=master
   :alt: Build Status
   :target: https://github.com/castle/castle-python/actions/workflows/specs.yml

The official Python SDK for `Castle <https://castle.io>`_. Castle analyzes user behavior in web and mobile apps to stop fraud before it happens.

This package is a thin wrapper around the `Castle HTTP API <https://reference.castle.io>`_. It exposes risk assessment, event logging, Lists, Privacy (GDPR), Events (enterprise), and webhook verification. See the API reference for supported events and payload shapes.

Requirements
------------

- Python 3.9 or newer
- A `Castle <https://dashboard.castle.io>`_ API secret

Installation
------------

.. code:: bash

    pip install castle

Quick start
-----------

.. code:: python

    import os
    from castle.configuration import configuration
    from castle.client import Client

    configuration.api_secret = os.environ['CASTLE_API_SECRET']

    client = Client.from_request(request)
    verdict = client.risk({
        'event': '$login',
        'status': '$succeeded',
        'request_token': request.POST.get('castle_request_token'),
        'user': {'id': '12345', 'email': 'user@example.com'},
    })

    action = verdict.get('policy', {}).get('action') or verdict.get('action')
    if action == 'deny':
        # block the user
        pass
    elif action == 'challenge':
        # send 2FA / additional verification
        pass
    else:
        # allow
        pass

``Client.from_request`` builds request context (IP, headers, client id) from a framework request object. See `Advanced configuration`_ for header allow/deny lists and proxy chains.

Configuration
-------------

The minimal, recommended setup:

.. code:: python

    import os
    from castle.configuration import configuration

    configuration.api_secret = os.environ['CASTLE_API_SECRET']

    # Behavior when Castle's API is unreachable or returns a 5xx.
    # One of: allow (default), deny, challenge, throw
    configuration.failover_strategy = 'allow'

    # Request timeout in milliseconds (default: 1000).
    # RequestError is raised on timeout.
    configuration.request_timeout = 1000

Logging
~~~~~~~

.. code:: python

    import logging
    from castle.configuration import configuration

    configuration.logger = logging.getLogger('castle')

The logger only needs to respond to ``info``. Each request and response is logged with sensitive values stripped.

Multi-environment / multi-tenant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most apps only need the global ``configuration`` singleton, but you can also create standalone ``Configuration`` instances and pass them per call via ``APIRequest``:

.. code:: python

    from castle.configuration import Configuration
    from castle.api_request import APIRequest
    from castle.commands.risk import CommandsRisk

    config = Configuration()
    config.api_secret = os.environ['CASTLE_API_SECRET_TENANT_A']

    APIRequest(config).call(CommandsRisk(context).call({
        'event': '$login',
        'status': '$succeeded',
        'request_token': '<token>',
        'user': {'id': '1234'},
    }))

Usage
-----

See `Castle documentation <https://docs.castle.io>`_ and the `API reference <https://reference.castle.io>`_ for endpoint details, event types, and integration guides.

Advanced configuration
----------------------

The defaults work for most deployments. The options below only matter if you have a non-trivial proxy chain or strict header policies.

Header allow/deny lists
~~~~~~~~~~~~~~~~~~~~~~~

By default the SDK sends every HTTP header except ``Cookie`` and ``Authorization``. Castle uses these headers to fingerprint the request.

.. code:: python

    from castle.configuration import configuration, DEFAULT_ALLOWLIST

    # Always-blocked headers (in addition to Cookie/Authorization).
    configuration.denylisted = ['HTTP-X-Internal-Header']

    # Strict allow-list mode. Headers outside the list are scrubbed,
    # except User-Agent which is always preserved.
    configuration.allowlisted = DEFAULT_ALLOWLIST

Header names are case-insensitive and accept both ``_`` and ``-`` as separators. A leading ``HTTP_`` prefix is stripped automatically.

Client IP detection
~~~~~~~~~~~~~~~~~~~

Castle needs the original client IP, not the IP of your proxy or load balancer. The SDK reads ``X-Forwarded-For`` and ``Remote-Addr`` by default; pick **one** of the strategies below:

.. code:: python

    from castle.configuration import configuration, TRUSTED_PROXIES

    # 1. Custom header (e.g. Cloudflare's Cf-Connecting-Ip).
    configuration.ip_headers = ['Cf-Connecting-Ip']

    # 2. Static, known proxy IPs (strings or regexes).
    configuration.trusted_proxies = ['10.0.0.1']

    # 3. Ephemeral proxies but known chain depth.
    configuration.trusted_proxy_depth = 2

    # 4. Last resort: trust the entire X-Forwarded-For chain.
    # Warning: vulnerable to header spoofing if a malicious proxy is in path.
    configuration.trust_proxy_chain = False

Use **either** ``trusted_proxies`` **or** ``trusted_proxy_depth``, not both. Private/loopback ranges in ``TRUSTED_PROXIES`` are always considered trusted.

Optional settings
~~~~~~~~~~~~~~~~~

.. code:: python

    from castle.configuration import configuration

    # Override the API base URL (default: https://api.castle.io/v1)
    # configuration.base_url = 'https://api.castle.io/v1'

Signature
---------

Secure mode signs user identifiers on the server:

.. code:: python

    from castle.secure_mode import signature

    signature(user_id)

Exceptions
----------

All exceptions inherit from ``CastleError``. The most useful ones:

- ``ConfigurationError`` — the SDK is misconfigured (missing API secret, invalid URL, etc.)
- ``RequestError`` — network failure or timeout reaching Castle
- ``InvalidRequestTokenError`` — the request token is missing or invalid
- ``InvalidParametersError`` — 422 response with validation details
- ``RateLimitError`` — 429 response; back off and retry
- ``UnauthorizedError`` — 401; bad API secret
- ``InternalServerError`` — 5xx response from Castle
- ``WebhookVerificationError`` — webhook signature did not match

The full list is in `castle/errors.py <https://github.com/castle/castle-python/blob/master/castle/errors.py>`_.
