Python SDK for Castle
=====================

.. image:: https://circleci.com/gh/castle/castle-python.svg?style=shield&branch=master
   :alt: Build Status
   :target: https://circleci.com/gh/castle/castle-python

`Castle <https://castle.io>`_ **analyzes device, location, and
interaction patterns in your web and mobile apps and lets you stop
account takeover attacks in real-time.**

Installation
------------

``pip install castle``

Configuration
-------------

Import and configure the library with your Castle API secret.

.. code:: python

    from castle.configuration import configuration, DEFAULT_ALLOWLIST

    # Same as setting it through Castle.api_secret
    configuration.api_secret = ':YOUR-API-SECRET'

    # For authenticate method you can set failover strategies: allow(default), deny, challenge, throw
    configuration.failover_strategy = 'deny'

    # Castle::RequestError is raised when timing out in milliseconds (default: 1000 milliseconds)
    configuration.request_timeout = 1500

    # Base Castle API url
    # configuration.base_url = "https://api.castle.io/v1"

    # Logger (need to respond to info method) - logs Castle API requests and responses
    # configuration.logger = logging.getLogger()

    # Allowlisted and Denylisted headers are case insensitive
    # and allow to use _ and - as a separator, http prefixes are removed
    # By default all headers are passed, but some are automatically scrubbed.
    # If you need to apply an allowlist, we recommend using the minimum set of
    # standard headers that we've exposed in the `DEFAULT_ALLOWLIST` constant.
    # Allowlisted headers
    configuration.allowlisted = DEFAULT_ALLOWLIST + ['X_HEADER']

    # Denylisted headers take advantage over allowlisted elements. Note that
    # some headers are always scrubbed, for security reasons.
    configuration.denylisted = ['HTTP-X-header']

    # Castle needs the original IP of the client, not the IP of your proxy or load balancer.
    # The SDK will only trust the proxy chain as defined in the configuration.
    # We try to fetch the client IP based on X-Forwarded-For or Remote-Addr headers in that order,
    # but sometimes the client IP may be stored in a different header or order.
    # The SDK can be configured to look for the client IP address in headers that you specify.

    # Sometimes, Cloud providers do not use consistent IP addresses to proxy requests.
    # In this case, the client IP is usually preserved in a custom header. Example:
    # Cloudflare preserves the client request in the 'Cf-Connecting-Ip' header.
    # It would be used like so: configuration.ip_headers=['Cf-Connecting-Ip']
    configuration.ip_headers = []

    # If the specified header or X-Forwarded-For default contains a proxy chain with public IP addresses,
    # then you must choose only one of the following (but not both):
    # 1. The trusted_proxies value must match the known proxy IPs. This option is preferable if the IP is static.
    # 2. The trusted_proxy_depth value must be set to the number of known trusted proxies in the chain (see below).
    # This option is preferable if the IPs are ephemeral, but the depth is consistent.

    # Additionally to make X-Forwarded-For and other headers work better discovering client ip address,
    # and not the address of a reverse proxy server, you can define trusted proxies
    # which will help to fetch proper ip from those headers

    # In order to extract the client IP of the X-Forwarded-For header
    # and not the address of a reverse proxy server, you must define all trusted public proxies
    # you can achieve this by listing all the proxies ip defined by string or regular expressions
    # in the trusted_proxies setting
    configuration.trusted_proxies = []
    # or by providing number of trusted proxies used in the chain
    configuration.trusted_proxy_depth = 0
    # note that you must pick one approach over the other.

    # If there is no possibility to define options above and there is no other header that holds the client IP,
    # then you may set trust_proxy_chain = true to trust all of the proxy IPs in X-Forwarded-For
    configuration.trust_proxy_chain = false
    # *Warning*: this mode is highly promiscuous and could lead to wrongly trusting a spoofed IP if the request passes through a malicious proxy

    # *Note: the default list of proxies that are always marked as "trusted" can be found in: Castle::Configuration::TRUSTED_PROXIES

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

    from castle.payload.prepare import PayloadPrepare
    from castle import events

    payload = PayloadPrepare.call(
        {
          'event': events.LOGIN_SUCCEEDED,
          'user_id': user.id,
          'properties': { 'key': 'value' },
          'user_traits': { 'key': 'value' }
        },
        request
    )

and use it later in a way

.. code:: python

    from castle.client import Client

    client = Client(context)
    client.track(options)

Events
--------------

List of Recognized Events can be found `here <https://github.com/castle/castle-python/tree/master/castle/events.py>`_ or in the `docs <https://docs.castle.io/api_reference/#list-of-recognized-events>`_.

Device management
-----------------

This SDK allows issuing requests to `Castle's Device Management
Endpoints <https://docs.castle.io/device_management_tool/>`__. Use these
endpoints for admin-level management of end-user devices (i.e., for an
internal dashboard).

Fetching device data, approving a device, reporting a device requires a
valid ``device_token``.

.. code:: python

    from castle.api.get_device import APIGetDevice

    # Get device data
    APIGetDevice.call(device_token)

.. code:: python

    from castle.api.approve_device import APIApproveDevice

    # Approve a device
    APIApproveDevice.call(device_token)

.. code:: python

    from castle.api.report_device import APIReportDevice

    # Report a device
    APIReportDevice.call(device_token)


Fetching available devices that belong to a given user requires a valid
``user_id``.

.. code:: python

    from castle.api.get_devices_for_user import APIGetDevicesForUser

    # Get user's devices data
    APIGetDevicesForUser.call(user_id)


Impersonation mode
------------------

https://castle.io/docs/impersonation_mode


Exceptions
----------

``CastleError`` will be thrown if the Castle API returns a 400 or a 500
level HTTP response. You can also choose to catch a more `finegrained
error <https://github.com/castle/castle-python/blob/master/castle/errors.py>`__.

Webhooks
--------

Castle uses webhooks to notify about ``$incident.confirmed`` or `$review.opened` events.
Each webhook has ``X-Castle-Signature`` header that allows verifying webhook's source.

.. code:: python

    from castle.webhooks.verify import WebhooksVerify

    # Verify the webhook, passed as a Request object
    WebhooksVerify.call(webhook)
    # WebhookVerificationError is raised when the signature is not matching


Documentation
-------------

Documentation and links to additional resources are available at
https://castle.io/docs

.. |Build Status| image:: https://travis-ci.org/castle/castle-python.svg?branch=master
   :target: https://travis-ci.org/castle/castle-python
