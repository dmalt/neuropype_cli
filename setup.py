from setuptools import setup

setup(
    name='neuropype_cli',
    version='0.1',
    py_modules=['neuropype'],
    author='cocolab',
    description='command line interface for neuropype_ephy',
    lisence='MIT',
    zip_sage=False,
    url='https://github.com/dmalt/neuropype_cli.git',
    install_requires=[
        'numpy',
        'mne',
        'nipype',
        'neuropype_ephy',
        'Click'
    ],
    entry_points='''
        [console_scripts]
        neuropype=neuropype:cli
    '''
)
