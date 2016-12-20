''' Command line interface for neuropype_ephy package '''
import click
import nipype.pipeline.engine as pe


@click.group(chain=True)
@click.option('--ncpu', '-n', default=1, help='number of CPUs to use')
@click.option('--plugin', '-p',
              type=click.Choice(['Linear', 'MultiProc', 'PBS']),
              default='MultiProc')
@click.option('--save-path', '-s', type=click.Path(), default='.', help='path to store results')
@click.option('--workflow-name', '-w', default='my_workflow',
              help='name of the results directory')
@click.option('--verbose', default=True)
def cli(ncpu, plugin, save_path, workflow_name, verbose):
    """Parallel processing of MEG/EEG data"""
    output_greeting()


# ---------------- Connect all the nodes into a workflow -------------------- #
@cli.resultcallback()
def process_pipeline(nodes, ncpu, plugin, save_path, workflow_name, verbose):
    """Create main workflow"""
    from nipype import config, logging

    input_node, path_node = nodes[-1]

    workflow = pe.Workflow(name=workflow_name)
    workflow.base_dir = (save_path)

    in_out = {'path_node': ('key', 'path'),
              'ep2ts': ('fif_file', 'ts_file'),
              'pwr': ('epochs_file', 'pwr_file'),
              'sp_conn': ('ts_file', 'conmat_file'),
              'mse': ('ts_file', 'mse_file'),
              'ica': ('fif_file', 'ica_file')}

    workflow.connect(input_node, 'keys', path_node, 'key')
    prev_node = path_node

    click.echo(click.style(input_node.name.upper(), fg='cyan'), nl=False)

    for node in nodes[:-1]:
        click.secho(' ---> {}'.format(node.name.upper()),
                    fg='cyan', nl=False)

        node.inputs.get()
        workflow.connect(prev_node, in_out[prev_node.name][1],
                         node, in_out[node.name][0])

        prev_node = node
    click.echo()
    # config.update_config({'logging': {'log_to_file': True}})
    # logging.update_logging(config)
    if verbose:
        if plugin == 'MultiProc':
            workflow.run(plugin='MultiProc', plugin_args={'n_procs': ncpu})
        elif plugin == 'Linear':
            workflow.run(plugin='Linear')
        elif plugin == 'PBS':
            workflow.run(plugin='PBS')
    else:
        from neuropype_ephy.aux_tools import suppress_stdout_stderr
        with suppress_stdout_stderr():
            if plugin == 'MultiProc':
                workflow.run(plugin='MultiProc', plugin_args={'n_procs': ncpu})
            elif plugin == 'Linear':
                workflow.run(plugin='Linear')
            elif plugin == 'PBS':
                workflow.run(plugin='PBS')
# -------------------------------------------------------------------------- #


# ------------------------------ Input node -------------------------------- #
@cli.command('input')
@click.argument('fif_files', nargs=-1, type=click.Path())
def infosrc(fif_files):
    ''' Create input node '''
    from os.path import abspath, split
    from os.path import commonprefix as cprfx
    from nipype.interfaces.utility import IdentityInterface, Function

    fif_files = [abspath(f) for f in fif_files]

    common_prefix = split(cprfx(fif_files))[0] + '/'
    iter_mapping = dict()
    for fif_file in fif_files:
        new_base = fif_file.replace(common_prefix, '')
        new_base = new_base.replace('/', '__')
        new_base = new_base.replace('.', '-')
        iter_mapping[new_base] = fif_file

    infosource = pe.Node(interface=IdentityInterface(fields=['keys']),
                         name='infosource')

    path_node = pe.Node(interface=Function(input_names=['key', 'iter_mapping'],
                                           output_names=['path'],
                                           function=map_path),
                        name='path_node')

    infosource.iterables = [('keys', iter_mapping.keys())]
    path_node.inputs.iter_mapping = iter_mapping
    return infosource, path_node
# ------------------------------------------------------------------------ #


# --------------------- Power spectral density node ---------------------- #
@cli.command('psd')
@click.option('--fmin', default=0., help='lower frequency bound')
@click.option('--fmax', default=300., help='higher frequency bound')
def psd(fmin, fmax):
    ''' Create power computation node '''
    from neuropype_ephy.interfaces.mne.power import Power
    # click.echo(list(fif_files))
    power = pe.Node(interface=Power(), name='pwr')
    power.inputs.fmin = fmin
    power.inputs.fmax = fmax
    power.inputs.method = 'welch'
    return power
# ------------------------------------------------------------------------- #


# --------------------------- Connectivity -------------------------------- #
@cli.command('conn')
@click.option('--band', '-b', nargs=2, type=click.Tuple([float, float]),
              multiple=True, help='frequency band')
@click.option('--method', '-m', nargs=1,
              type=click.Choice(["coh", "imcoh", "plv", "pli",
                                 "wpli", "pli2_unbiased",
                                 "ppc", "cohy", "wpli2_debiased"]),
              default=('imcoh',), multiple=True, help='connectivity measure')
@click.option('--sfreq', '-s', nargs=1, type=click.INT,
              help='data sampling frequency')
def connectivity(band, method, sfreq):
    """Create spectral connectivity node"""
    from neuropype_ephy.interfaces.mne.spectral import SpectralConn
    # if not method:
    #     method = ('imcoh',)
    freq_bands = [list(t) for t in band]

    sp_conn = pe.Node(interface=SpectralConn(), name='sp_conn')
    # sp_conn.inputs.con_method = con_method
    sp_conn.inputs.sfreq = sfreq
    sp_conn.iterables = [('freq_band', freq_bands), ('con_method', method)]
    return sp_conn
# ------------------------------------------------------------------------- #


# --------------------- Epochs to timeseries node ------------------------- #
@cli.command('ep2ts')
def fif_ep_2_ts():
    ''' Create a node for epochs 2 npy timeseries conversion '''

    from neuropype_ephy.nodes.import_data import Ep2ts
    ep2ts = pe.Node(interface=Ep2ts(), name='ep2ts')
    return ep2ts
# ------------------------------------------------------------------------- #


# -------------------------- Multiscale entropy node ---------------------- #
@cli.command('mse')
@click.option('-m', default=2)
@click.option('-r', default=0.2)
def multiscale(m, r):
    """Create multiscale entropy node"""
    from neuropype_ephy.mse import get_mse_multiple_sensors
    from nipype.interfaces.utility import Function
    mse = pe.Node(interface=Function(input_names=['ts_file', 'm', 'r'],
                                     output_names=['mse_file'],
                                     function=get_mse_multiple_sensors),
                  name='mse')

    mse.inputs.m = m
    mse.inputs.r = r
    return mse
# ------------------------------------------------------------------------- #


# --------------------------- ICA node ------------------------------------ #
@cli.command('ica')
@click.option('--n-components', '-n', default=50.)
@click.option('--ecg-ch-name', '-c', type=click.STRING, default='')
@click.option('--eog-ch-name', '-o', type=click.STRING, default='')
def ica(n_components, ecg_ch_name, eog_ch_name):
    """Compute ica solution for raw fif file"""
    from neuropype_ephy.interfaces.mne.preproc import CompIca
    ica_node = pe.Node(interface=CompIca(), name='ica')
    ica_node.inputs.n_components = n_components
    ica_node.inputs.ecg_ch_name = ecg_ch_name
    ica_node.inputs.eog_ch_name = eog_ch_name
    return ica_node
# ------------------------------------------------------------------------- #


def map_path(key, iter_mapping):
    """Map paths"""
    return iter_mapping[key]


def output_greeting():
    """Output greeting"""

    click.echo(click.style(r'''
  _  _ ___ _   _ ___  ___  _____   _____ ___
 | \| | __| | | | _ \/ _ \| _ \ \ / / _ \ __|
 | .` | _|| |_| |   / (_) |  _/\ V /|  _/ _|
 |_|\_|___|\___/|_|_\\___/|_|   |_| |_| |___|''', fg='magenta'))
    click.echo(click.style(r'''
                _.-'-'--._
               ,', ~'` ( .'`.
              ( ~'_ , .'(  >-)
             ( .-' (  `__.-<  )
              ( `-..--'_   .-')
               `(_( (-' `-'.-)
                   `-.__.-'=/
                      `._`='
                         \\''', fg='magenta'))

