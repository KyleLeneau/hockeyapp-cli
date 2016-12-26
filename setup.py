from setuptools import setup, find_packages

setup(
    name='hockeyapp-cli',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        hockeyapp=hockeyapp.cli:cli
    ''',
)