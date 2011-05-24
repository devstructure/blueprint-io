from setuptools import setup, find_packages

setup(name='blueprint_io',
      version='__VERSION__',
      description='centralized blueprint service client',
      author='Richard Crowley',
      author_email='richard@devstructure.com',
      url='http://devstructure.com/',
      packages=find_packages(),
      install_requires=['blueprint'],
      license='BSD',
      zip_safe=False)
