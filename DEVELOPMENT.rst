Installation
------------

.. code-block:: console

    $ git clone git@github.com:castle/castle-python.git
    $ cd castle-python
    $ python3 setup.py install


Test
------------

.. code-block:: console

    $ python3 setup.py test

Linting
------------

.. code-block:: console

    $ pip3 install pylint
    $ pip3 install --upgrade pep8
    $ pip3 install --upgrade autopep8
    $ pylint --rcfile=./pylintrc castle
    $ autopep8 --in-place -r castle

Coverage
------------

.. code-block:: console

    $ pip3 install coverage
    $ coverage run setup.py test
