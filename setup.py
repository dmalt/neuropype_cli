from setuptools import setup

setup(
    name='neuropype_cli',
    version='0.1.1',
    author='Dmitrii Altukhov',
    authou_email='dm.altukhov@ya.ru',
    description='command line interface for neuropype_ephy',
    lisence='MIT',
    zip_safe=False,
    packages=['neuropype_cli'],
    url='https://github.com/dmalt/neuropype_cli.git',
    dependency_links=['https://github.com/dmalt/neuropype_ephy/tarball/dev#egg=neuropype_ephy'],
    install_requires=[
        'numpy',
        'mne',
        'nipype',
        'Click',
        'configparser',
        'neuropype_ephy'
    ],
    entry_points='''
        [console_scripts]
        neuropype=neuropype_cli.neuropype:cli
    '''
)
