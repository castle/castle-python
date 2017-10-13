Releasing
=========

1. Update `VERSION` in `castle/version.py` to the new version
2. Update the `HISTORY.md` for the impending release
3. `git commit -am "prepare for release X.Y.Z."` (where X.Y.Z is the new version)
4. `git tag -a vX.Y.Z -m "release X.Y.Z"` (where X.Y.Z is the new version)
5. `git push --tags`
6. `rm -rf dist`
7. `python3 setup.py sdist bdist_wheel`
8. `twine upload dist/*`


When you change something in the README.rst make sure it is in the correct format, as pypi
will ignore the file if it is not valid.

`pip3 install collective.checkdocs`
`pip3 install pygments`
`python3 setup.py checkdocs`

To upload to testpypi `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
