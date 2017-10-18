Python SDK for Castle
=====================


.. image:: https://travis-ci.org/castle/castle-python.png
   :alt: Build Status
   :target: https://travis-ci.org/castle/castle-python


`Castle <https://castle.io>`_ analyzes device, location, and interaction patterns in your web and mobile apps and lets you stop account takeover attacks in real-time.


Here is a simple example of track event.

.. code-block:: python

    from castle.configuration import configuration
    from castle.client import Client

    configuration.api_secret = ':YOUR-API-SECRET'

    castle = Client(request, {})
    castle.track(
        {
            'event': '$login.succeeded',
            'user_id': 'user_id'
        }
    )
    

Documentation
-------------


Documentation and links to additional resources are available at
https://castle.io/docs
