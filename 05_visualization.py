from swann.utils import (get_config, get_layout,
                         exclude_subjects, get_behf)
from swann.viz import plot_beta_bursting, plot_power

config = get_config()
layout = get_layout()

eegfs = (layout.get(task=config['task'],
                    suffix='eeg', extension='bdf') +
         layout.get(task=config['task'],
                    suffix='eeg', extension='vmrk'))
eegfs = exclude_subjects(eegfs)

overwrite = \
    input('Overwrite plots if they exist? (y/n)\n').upper() == 'Y'

# loop across subjects
for eegf in eegfs:
    behf = get_behf(eegf)
    plot_beta_bursting(eegf, behf, overwrite=overwrite)
    plot_power(eegf, behf, overwrite=overwrite)
