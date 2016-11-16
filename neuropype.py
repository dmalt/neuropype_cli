import click
from power_workflow import create_main_workflow_power
import nipype.pipeline.engine as pe



@click.group(chain=True, invoke_without_command=True)
# @click.option('--ncpu', default=1)
# @click.pass_context
def cli():
    # ctx.obj = ncpu
    pass

@cli.resultcallback()
def process_pipeline(nodes):
    ''' Create main workflow '''
    click.echo(nodes)
    in_node = nodes[-1]
    pwr_node = nodes[-2]

    workflow = pe.Workflow(name='test')
    workflow.connect(in_node, 'fif_files', pwr_node, 'epochs_file')
    workflow.run(plugin='MultiProc', plugin_args={'n_procs' : 8})

@cli.command('pwr')
# @click.argument('fif_files', nargs=-1, type=click.Path())
# @click.option('--dest-path', '-dp')
def pwr():
    ''' Create power computation node '''
    from neuropype_ephy.interfaces.mne.power import Power
    # click.echo(list(fif_files))
    power = pe.Node(interface=Power(), name='pwr')
    power.inputs.fmin = 0
    power.inputs.fmax = 300
    power.inputs.method = 'welch'
    return power


@cli.command('input')
@click.argument('fif_files', nargs=-1, type=click.Path())
def infosrc(fif_files):
    ''' Create input node '''
    from nipype.interfaces.utility import IdentityInterface
    infosource = pe.Node(interface=IdentityInterface(fields=['fif_files']), name='infosource')
    infosource.iterables = [('fif_files', fif_files)]
    return infosource




@cli.command('connectivity')
def connectivity():
    ''' Create spectral connectivity node '''
    click.echo('Nokia: connecting people')


# cli.add_command(pwr)
# cli.add_command(input)
# cli.add_command(connectivity)

# if __name__ == '__main__':
#     cli(obj={})
