# Description

Command line interface for neuropype_ephy package

# Installation

## Requirements
For now CLI works only with python2; python3 compatibility is planned for later releases

* Click
* numpy
* scikit-learn
* mne
* nipype
* neuropype_ephy

Some of these dependencies you should install manually (see "Install dependencies 
with conda") and others are installed automatically during neuropype_cli installation

## Install dependencies with conda
```bash
$ conda install numpy
$ conda install scikit-learn
```

Or if you have installed anaconda distribution these packages are already included 

## Install package
### Install neuropype_ephy
```bash
$ git clone https://github.com/dmalt/neuropype_ephy.git
$ cd neuropype_ephy
$ pip install .
```
### Install neuropype_cli
```bash
$ git clone https://github.com/dmalt/neuropype_cli.git
$ cd neuropype_cli
$ pip install .
```
