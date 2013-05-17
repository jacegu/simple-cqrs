try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'simplecqrs',
    'description': "Port of Greg Young's m-r to python",
    'author': 'Javier Acero',
    'url': 'http://github.com/jacegu/simple-cqrs',
    'download_url': 'http://github.com/jacegu/simple-cqrs',
    'author_email': 'j4cegu@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['simplecqrs'],
    'scripts': []
}

setup(**config)
