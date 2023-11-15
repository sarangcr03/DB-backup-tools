from setuptools import setup, find_packages

setup(
    name='mysqlbc',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mysqlbc=mysqlbc.mysql_backup:main',
        ],
    },
    install_requires=[
        'python-dotenv',
    ],
)