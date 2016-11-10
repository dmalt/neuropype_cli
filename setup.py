from setuptools import setup

setup(
    name='neuropype',
    version='0.1',
    py_modules=['neuropype'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        neuropype=neuropype:cli
    ''',
)
