# Description
---------------

Command line interface for neuropype_ephy package

# Installation
---------------
## Requirements

python2 - this requirement is temporary and is caused by neuropype_ephy package which is
not python3 compatible for now

Click

numpy

scikit-learn

mne

nipype

neuropype_ephy

Some of these dependencies you should install manually (see "Install dependencies 
with conda") and others are installed automatically during neuropype_cli installation

## Install dependencies with conda

$ conda install numpy

$ conda install scikit-learn

Or if you have installed anaconda distribution these packages are already included 

## Install package

This command will install neuropype_cli with all remaining dependencies automatically:

$ pip install neuropype_cli -r requirements.txt
