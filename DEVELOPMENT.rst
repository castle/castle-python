Development
===========

Requirements
------------

Python 3.9 or newer. The repo pins a version in ``.tool-versions``; with `asdf` installed, run commands via ``asdf exec`` (or ensure that Python is active in your shell).

Installation
------------

.. code-block:: console

    $ git clone git@github.com:castle/castle-python.git
    $ cd castle-python
    $ make setup

``make setup`` installs the package in editable mode with test and lint extras (``pip install -e ".[test,lint]"``).

Test
----

.. code-block:: console

    $ make test

Runs ``python3 -m unittest -v castle.test``. CI runs the same suite on Python 3.9–3.13 via GitHub Actions (``.github/workflows/specs.yml``).

Linting
-------

.. code-block:: console

    $ make lint

Runs ``ruff check`` and ``ruff format --check`` on ``castle/``. CI uses the same checks (``.github/workflows/lint.yml``).

To auto-fix and format:

.. code-block:: console

    $ make format

Coverage
--------

.. code-block:: console

    $ make coverage

Makefile targets
----------------

``make help`` lists ``setup``, ``test``, ``lint``, ``format``, and ``coverage``.
