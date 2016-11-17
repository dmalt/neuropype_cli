''' Command line interface for neuropype_ephy package '''
import click
import nipype.pipeline.engine as pe



@click.group(chain=True)
@click.option('--ncpu', '-n', default=1, help='number of CPUs to use')
@click.option('--plugin', '-p', type=click.Choice(['Linear', 'MultiProc', 'PBS']),
              default='MultiProc')
@click.option('--save-path', '-s', default='.', help='path to store results') 
@click.option('--workflow-name', '-w', default='my_workflow')
# @click.pass_context
def cli(ncpu, plugin, save_path, workflow_name):
    ''' Parallel processing of MEG/EEG data '''
    # ctx.obj = ncpu
    pass


@cli.resultcallback()
# @click.pass_context
def process_pipeline(nodes, ncpu, plugin, save_path, workflow_name):
    ''' Create main workflow '''
    input_node, path_node = nodes[-1]
    # pwr_node = nodes[-2]

    workflow = pe.Workflow(name=workflow_name)
    workflow.base_dir = save_path
    # workflow.connect(in_node, 'fif_files', pwr_node, 'epochs_file')


    in_out = {'path_node': ('key', 'path'),
              'ep2ts': ('fif_file', 'ts_file'),
              'pwr': ('epochs_file', 'pwr_file'),
              'sp_conn': ('ts_file', 'conmat_file')}
    workflow.connect(input_node, 'keys', path_node, 'key')
    prev_node = path_node

    for node in nodes[:-1]:
        click.echo(node)
        node.inputs.get()
        workflow.connect(prev_node, in_out[prev_node.name][1], node, in_out[node.name][0])
        prev_node = node

    click.echo(plugin)

    if plugin == 'MultiProc':
        workflow.run(plugin='MultiProc', plugin_args={'n_procs' : ncpu})
    elif plugin == 'Linear':
        workflow.run(plugin='Linear')
    elif plugin == 'PBS':
        workflow.run(plugin='PBS')


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


@cli.command('input')
@click.argument('fif_files', nargs=-1, type=click.Path())
def infosrc(fif_files):
    ''' Create input node '''
    from os.path import abspath, split, splitext, join
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


    infosource = pe.Node(interface=IdentityInterface(fields=['keys']), name='infosource')

    path_node = pe.Node(interface=Function(input_names=['key', 'iter_mapping'], output_names=['path'],
                                           function=map_path), name='path_node')

    infosource.iterables = [('keys', iter_mapping.keys())]
    path_node.inputs.iter_mapping = iter_mapping 
    return infosource, path_node

def map_path(key, iter_mapping):
    return iter_mapping[key]

# --------------------------- Connectivity ----------------------------------- #
@cli.command('conn')
@click.option('--band', '-b', nargs=2, type=click.Tuple([float, float]),
              multiple=True, help='frequency band')
@click.option('--method', '-m', nargs=1, type=click.Choice(["coh", "imcoh", "plv", "pli",
                                                            "wpli", "pli2_unbiased",
                                                            "ppc", "cohy", "wpli2_debiased"]),
              default=('imcoh',), multiple=True, help='connectivity measure')
def connectivity(band, method):
    ''' Create spectral connectivity node '''
    from neuropype_ephy.interfaces.mne.spectral import SpectralConn
    # if not method:
    #     method = ('imcoh',)
    sfreq = 1000
    freq_bands = [list(t) for t in band]

    sp_conn = pe.Node(interface=SpectralConn(), name='sp_conn')
    # sp_conn.inputs.con_method = con_method
    sp_conn.inputs.sfreq = sfreq
    sp_conn.iterables = [('freq_band', freq_bands), ('con_method', method)]
    return sp_conn
# ----------------------------------------------------------------------------- #


@cli.command('ep2ts')
def fif_ep_2_ts():
    ''' Create a node for epochs 2 npy timeseries conversion '''

    from neuropype_ephy.nodes.import_data import Ep2ts
    ep2ts = pe.Node(interface=Ep2ts(), name='ep2ts')
    return ep2ts

