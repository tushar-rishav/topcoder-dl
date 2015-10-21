try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
setup(name='topcoder-dl',
      version='0.0.2',
      install_requires=[
          r for r in open('requirements.txt', 'r').read().split('\n') if r],
      author='Tushar Gautam',
      author_email='tushar.rishav@gmail.com',
      packages=['TopcoderDl', ],
      entry_points={
          'console_scripts': ['topcoderdl=TopcoderDl:main'],
      },
      license='GNU General Public License v3 (GPLv3)',
      url='https://github.com/tushar-rishav/topcoder-dl/',
      description="Downloads all TopCoder data-science tutorials and save as PDF",
      long_description=open('README.rst').read(),
      keywords=['pdf', 'algorithms','tutorials', 'Topcoder', 'python', 'scrapping'],
      classifiers=[
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Monitoring'
      ],
      )