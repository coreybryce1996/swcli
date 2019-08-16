
from setuptools import setup

setup(
    name='starwars',
    version='0.1',
    py_modules=['starwars'],
    install_requires=[
        'Click',
        'requests',
        '--editable .'
    ],
    entry_points='''
        [console_scripts]
        starwars=starwars:cli
        ''',
)
