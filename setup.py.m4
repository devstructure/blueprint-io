from setuptools import setup

setup(name='blueprint-io',
      version='__VERSION__',
      description='centralized blueprint service client',
      author='Richard Crowley',
      author_email='richard@devstructure.com',
      url='http://devstructure.com/',
      packages=['blueprint.io'],
      install_requires=['blueprint'],
      license='BSD',
      zip_safe=False)
