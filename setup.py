try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests>=2.5',
    ],
    tests_require=['responses'],
    test_suite='castle.test.all'
)
