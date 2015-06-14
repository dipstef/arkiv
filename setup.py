from setuptools import setup

settings = {}

settings.update(
    name='arkiv',
    version='0.1',
    description='Archive file names',
    author='Stefano Dipierro',
    url='https://github.com/dipstef/arkiv',
    packages=['arkiv'],
    test_suite='tests',
    requires=['urlo', 'unicoder']
)

setup(**settings)