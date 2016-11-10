import click
from power_workflow import create_main_workflow_power


@click.group()
@click.option('--ncpu')
@click.pass_context
def cli(ctx, ncpu):
    ctx.obj = ncpu
    pass


@click.command()
@click.argument('fif_files')
@click.option('--dest-path', '-dp')
@click.pass_context
def power(ctx, fif_files, dest_path):
    workflow = create_main_workflow_power(fif_files)
    main_workflow.run(plugin='MultiProc', plugin_args={'n_procs' : ctx.obj})



@click.command()
def connectivity():
    click.echo('Nokia: connecting people')


cli.add_command(power)
cli.add_command(connectivity)

# if __name__ == '__main__':
#     cli(obj={})
