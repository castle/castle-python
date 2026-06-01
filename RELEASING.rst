Releasing
=========

#. Create release branch ``X.Y.Z`` from ``develop``.
#. Update ``VERSION`` in ``castle/version.py`` to the new version
#. Update the ``CHANGELOG.rst`` for the impending release
#. ``git commit -am "release X.Y.Z"`` (where X.Y.Z is the new version)
#. Push to Github, make PR to the develop branch, and when approved, merge.
#. Pull latest ``develop``, merge it to ``master``, and push it.
#. Make a release on Github from the ``master`` branch, specify tag as ``vX.Y.Z`` to create a tag.
#. ``git checkout master && git pull``
#. ``rm -rf dist build``
#. ``python3 -m build``
#. ``twine upload dist/*``

When you change something in the README.rst make sure it is in the
correct format, as pypi will ignore the file if it is not valid.

To validate the rendered metadata locally:

``pip3 install build twine``

``python3 -m build && twine check dist/*``

To upload to testpypi
``twine upload --repository-url https://test.pypi.org/legacy/ dist/*``
