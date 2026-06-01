Installation
------------

.. code-block:: console

    $ git clone git@github.com:castle/castle-python.git
    $ cd castle-python
    $ pip3 install -e ".[test,lint]"


Test
------------

.. code-block:: console

    $ python3 -m unittest castle.test

Linting
------------

.. code-block:: console

    $ pip3 install ruff
    $ ruff check castle
    $ ruff format --check castle

To auto-fix and format:

.. code-block:: console

    $ ruff check --fix castle
    $ ruff format castle

Coverage
------------

.. code-block:: console

    $ pip3 install coverage
    $ coverage run -m unittest castle.test
    $ coverage report
