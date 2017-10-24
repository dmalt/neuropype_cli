Neuroclick
==========

Command line interface for [neuropype_ephy]( https://github.com/dmalt/neuropype_ephypackage)
package and more wrapping up some mne-python functions with powerful nipype framework.

Getting started
------------

### Prerequisites
For now CLI works only with python2; python3 support might also happen in the future.

Full list of dependencies can be found [here](https://github.com/dmalt/neuropype_cli/commit/1621265f8b43d901a25c12ac863b31c98f2d8b58).

No need to install them manually though. All dependencies are installed
automatically during the *Installation* step

### Installation

1) First, clone the package sources and go inside the project folder:
    ```bash
    git clone https://github.com/dmalt/neuropype_cli.git
    cd neuropype_cli
    ```
2) The simplest way to install the package is as follows:
    ```bash
    pip install .
    cd ..
    ```

    But it is strongly recommended to install *neuroclick* under virtual environement so the dependencies
    don't damage your current python setup.

    To do so perform the following steps:

    * [Install virtualenv package](https://virtualenv.pypa.io/en/stable/installation/)
      if it's not already in your system
    * Think of a name for your virtual environement (i.e. neuroenv) and
      create virtual environement inside the project folder by running 
        ```bash
        virtualenv neuroenv
        ```
    * Activate your virtual environement:
      ```bash
      source ./neuroenv/bin/activate
      ```
    * Perform the installation (note the '.' symbol in the end):
      ```bash
      pip install .
      cd .. # exit from the project folder
      ```

If you've been using virtualenv you should activate it each time you are running neuroclick

3) You can check the installation by running 
    ```bash
    neuropype --help
    ```


Documentation
--------------
[For quick ref check out my presentation on neuropype_cli package](https://github.com/dmalt/neuropype_cli/blob/master/main.pdf)

Detailed documentation can be found [here](http://neuropype-cli.readthedocs.io/en/latest/)
