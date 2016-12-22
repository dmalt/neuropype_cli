from setuptools import setup

setup(
    name='neuropype_cli',
    version='0.1.1',
    author='Dmitrii Altukhov',
    author_email='dm.altukhov@ya.ru',
    description='command line interface for neuropype_ephy',
    license='MIT',
    zip_safe=False,
    packages=['neuropype_cli'],
    url='https://github.com/dmalt/neuropype_cli.git',
    install_requires=[
        'mne',
        'nipype',
        'Click',
        'configparser'
    ],
    entry_points='''
        [console_scripts]
        neuropype=neuropype_cli.neuropype:cli
    '''
)
