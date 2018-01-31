from setuptools import find_packages, setup

from castle.version import VERSION


setup(
    name="castle",
    version=VERSION,
    author="Castle Intelligence, Inc.",
    author_email="info@castle.io",
    license="MIT License",
    description="Castle protects your users from account compromise",
    long_description=open("README.rst").read(),
    url="https://github.com/castle/castle-python",
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['requests>=2.5'],
    extras_require={
        'test': ['responses'],
    },
    # A better way to specify test requirements
    # see https://github.com/pypa/pip/issues/1197#issuecomment-228939212
    tests_require=['castle[test]'],
    test_suite='castle.test.all'
)
