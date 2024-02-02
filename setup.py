# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foss505', 'foss505.ui']

package_data = \
{'': ['*'], 'foss505.ui': ['assets/fonts/*', 'assets/images/*']}

install_requires = \
['jack-client>=0.5.4,<0.6.0', 'numpy>=1.24.1,<2.0.0']

extras_require = \
{':python_version >= "3.10" and python_version < "3.12"': ['PySide6==6.4.1']}

entry_points = \
{'console_scripts': ['foss505 = foss505:run']}

setup_kwargs = {
    'name': 'foss505',
    'version': '0.1.0a0',
    'description': 'The ultimate loop station.',
    'author': 'reo6',
    'author_email': 'ramazanemre@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reo6/foss505',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
