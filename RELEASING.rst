Releasing
=========

#. Create release branch ``X.Y.Z`` from ``main``.
#. Update ``VERSION`` in ``castle/version.py`` to the new version.
#. Update ``CHANGELOG.rst`` for the impending release.
#. ``git commit -am "release X.Y.Z"`` (where ``X.Y.Z`` is the new version).
#. Push to GitHub, open a PR to ``main``, and merge when approved.
#. On ``main``: run ``make test`` and ``make lint`` (or confirm CI is green).
#. Create a GitHub release from ``main`` with tag ``vX.Y.Z`` (see below).
#. Publish to PyPI from ``main`` (see below). A GitHub release does **not** publish the package; PyPI is updated only via ``twine upload``.

GitHub release
--------------

Create the release only after ``main`` on ``origin`` contains the release commit.

.. code-block:: console

    gh release create vX.Y.Z \
      --title "Release X.Y.Z" \
      --notes-file release-notes.md

Use ``--latest`` as a separate flag if you need to mark the release as Latest; do not put ``--latest`` in ``--title``.

PyPI
----

From a clean checkout of ``main`` at the release commit:

.. code-block:: console

    git checkout main && git pull
    rm -rf dist build
    pip install build twine
    python3 -m build
    twine check dist/*
    twine upload dist/*

README and metadata
-------------------

When you change ``README.rst``, validate that PyPI will accept it:

.. code-block:: console

    python3 -m build && twine check dist/*

PyPI ignores ``README.rst`` if it is not valid reStructuredText.

TestPyPI
--------

.. code-block:: console

    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
