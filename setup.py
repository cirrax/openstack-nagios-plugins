from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openstacknagios',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='1.0.1',

    description='nagios/icinga plugins to monitor an openstack installation',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/cirrax/openstack-nagios-plugins',

    # Author details
    author='Benedikt Trefzer',
    author_email='benedikt.trefzer@cirrax.com',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: System :: Monitoring',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='openstack icinga nagios check',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=[
        'nagiosplugin', 
        'python-novaclient', 
        'python-keystoneclient', 
        'python-neutronclient', 
        'python-cinderclient',
        'python-ceilometerclient',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'check_nova-services=openstacknagios.nova.Services:main',
            'check_nova-hypervisors=openstacknagios.nova.Hypervisors:main',
            'check_cinder-services=openstacknagios.cinder.Services:main',
            'check_neutron-agents=openstacknagios.neutron.Agents:main',
            'check_neutron-floatingips=openstacknagios.neutron.Floatingips:main',
            'check_keystone-token=openstacknagios.keystone.Token:main',
            'check_ceilometer-statistics=openstacknagios.ceilometer.Statistics:main',
        ],
    },
)
