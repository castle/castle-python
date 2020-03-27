Releasing
=========

1. Create branch `X.Y.Z`.
2. Update `VERSION` in `castle/version.py` to the new version
3. Update the `HISTORY.md` for the impending release
4. `git commit -am "release X.Y.Z"` (where X.Y.Z is the new version)
5. Push to Github, make PR, and when ok, merge.
6. Make a release on Github, specify tag as `vX.Y.Z` to create a tag.
7. `git checkout master && git pull`
8. `rm -rf dist`
9. `python3 setup.py sdist bdist_wheel`
10. `twine upload dist/*`


When you change something in the README.rst make sure it is in the correct format, as pypi
will ignore the file if it is not valid.

`pip3 install collective.checkdocs`

`pip3 install pygments`

`python3 setup.py checkdocs`

To upload to testpypi `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
