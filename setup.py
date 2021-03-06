#!/usr/bin/env python
from setuptools import setup, find_packages
import pkg_resources
import sys
import os

try:
    if int(pkg_resources.get_distribution("pip").version.split('.')[0]) < 6:
        print('pip older than 6.0 not supported, please upgrade pip with:\n\n'
              '    pip install -U pip')
        sys.exit(-1)
except pkg_resources.DistributionNotFound:
    pass

if os.environ.get('CONVERT_README'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
else:
    long_description = ''

version = sys.version_info[:2]
if version < (2, 7):
    print('dwim requires Python version 2.7 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)
elif (3, 0) < version < (3, 3):
    print('dwim requires Python version 3.3 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

VERSION = '3.11'

install_requires = ['psutil', 'colorama', 'six', 'decorator']
extras_require = {':python_version<"3.4"': ['pathlib2'],
                  ":sys_platform=='win32'": ['win_unicode_console']}

setup(name='dwim',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      long_description=long_description,
      author='Vladimir Iakovlev',
      author_email='aoeu.rm@gmail.com',
      url='https://github.com/aoeu/dwim',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'tests.*', 'release']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points={'console_scripts': [
          'dwim = dwim.main:main',
          'dwim = dwim.main:how_to_configure_alias']})
