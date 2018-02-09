# Python SDK for Castle

[![Build Status](https://travis-ci.org/castle/castle-python.svg?branch=master)](https://travis-ci.org/castle/castle-python)

**[Castle](https://castle.io) analyzes device, location, and interaction patterns in your web and mobile apps and lets you stop account takeover attacks in real-time.**

## Installation

`pip install castle`

## Configuration

import and configure the library with your Castle API secret.

```python
    from castle.configuration import configuration

    # Same as setting it through Castle.api_secret
    configuration.api_secret = ':YOUR-API-SECRET'

    # For authenticate method you can set failover strategies: allow(default), deny, challenge, throw
    configuration.failover_strategy = 'deny'

    # Castle::RequestError is raised when timing out in seconds (default: 0.5 of the second)
    configuration.request_timeout = 1

    # Whitelisted and Blacklisted headers are case insensitive and allow to use _ and - as a separator, http prefixes are removed
    # Whitelisted headers
    configuration.whitelisted = ['X_HEADER']
    # or append to default
    configuration.whitelisted = configuration.whitelisted + ['http-x-header']

    # Blacklisted headers take advantage over whitelisted elements
    configuration.blacklisted = ['HTTP-X-header']
    # or append to default
    configuration.blacklisted = configuration.blacklisted + ['X_HEADER']
```

## Tracking

Here is a simple example of track event.

```python
    from castle.client import Client

    castle = Client.from_request(request)
    castle.track(
        {
            'event': '$login.succeeded',
            'user_id': 'user_id'
        }
    )
```
The client will automatically configure the context for each request.

## Signature

```python

    from secure_mode import signature

    signature(user_id)
```

will create a signed user_id.

## Async tracking

By default Castle sends requests synchronously. To send requests in a background worker you can generate data for a worker:

```python
    from castle.client import Client

    context = Client.to_context(request)
    options = Client.to_options({
      'event': '$login.succeeded',
      'user_id': user.id,
      'properties': {
        'key': 'value'
      },
      'traits': {
        'key': 'value'
      }
    })
```

and use it later in a way

```python
    from castle.client import Client

    client = Client(context)
    client.track(options)
```

## Exceptions

`CastleError` will be thrown if the Castle API returns a 400 or a 500 level HTTP response. You can also choose to catch a more [finegrained error](https://github.com/castle/castle-python/blob/master/castle/exceptions.py).

## Documentation

Documentation and links to additional resources are available at
https://castle.io/docs
