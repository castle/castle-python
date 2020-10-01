try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

import sys
from castle.version import VERSION

install_requires = ['requests>=2.5']
test_require = ['responses']

if sys.version_info[:2] == (3, 4):
    test_require.append('urllib3>=1.21.1,<1.25')

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=install_requires,
    tests_require=test_require,
    test_suite='castle.test.all'
)
