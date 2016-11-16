def create_main_workflow_power(fif_files):

    import nipype.pipeline.engine as pe
    from nipype.interfaces.utility import IdentityInterface
    from neuropype_ephy.interfaces.mne.power import Power
    import nipype.interfaces.io as nio
    power_analysis_name = 'test'
    main_workflow = pe.Workflow(name=power_analysis_name)
    main_workflow.base_dir = '/media/dmalt/SSD500/'

    data_source = pe.Node(interface=IdentityInterface(fields=['fif_files']), 
                                                     name='data_source')
    data_source.iterables = [('fif_files', fif_files)] 

    ## Info source
    power_node = pe.Node(interface=Power(), name='pwr')
    power_node.inputs.fmin = 0;
    power_node.inputs.fmax = 300;
    power_node.inputs.method = 'welch'

    main_workflow.connect(data_source, 'fif_files', power_node, 'epochs_file')
    return main_workflow

# def main():
#     pipeline = pe.Workflow(name='test')
#     pipeline.base_dir = './'
#     epochs_file = '/home/dmalt/Github/python/pipeline/neuropype_ephy/neuropype_ephy/tests/test-epo.fif'
#     test_node = pe.Node(interface=Power(), name='pwr')
#     test_node.inputs.epochs_file = epochs_file
#     test_node.run()

if __name__ == '__main__':
    main_workflow = create_main_workflow_power()
    main_workflow.run(plugin='MultiProc', plugin_args={'n_procs' : 8})
