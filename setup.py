# coding: utf-8
import sys

from setuptools import setup, find_packages

install_requires = [
]

if sys.version_info < (2, 7):
    install_requires.append('importlib')
    install_requires.append('logutils')
    install_requires.append('ordereddict')

with open('README.md') as f:
    long_description = f.read()

setup(
    name='streamsaver',
    version='1.0.2',
    url='http://localhost',
    license='',
    description=('Saves RTPS, UDP, TCP video stream into local files'),
    long_description=long_description,
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
    },
    zip_safe=False,
    platforms='any',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ),
    entry_points={
    'console_scripts': [
        'transform=streamsaver.main:main',
    ],
},
    test_suite='test',
)
