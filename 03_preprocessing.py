from swann.utils import (get_config, get_layout,
                         exclude_subjects, my_events)
from swann.preprocessing import find_ica, apply_ica, mark_autoreject
from swann.viz import plot_find_bads, plot_ica

config = get_config()
layout = get_layout()

eegfs = (layout.get(task=config['task'],
                    suffix='eeg', extension='bdf') +
         layout.get(task=config['task'],
                    suffix='eeg', extension='vmrk'))
eegfs = exclude_subjects(eegfs)

overwrite_eeg = \
    input('Overwrite preprocessed eeg data if ' +
          'they exist? (y/n)\n').upper() == 'Y'

# loop across subjects
for eegf in eegfs:
    plot_find_bads(eegf, overwrite=overwrite_eeg)

# this will probably take ~5 minutes per subject, probably come back later
for eegf in eegfs:
    find_ica(eegf, overwrite=overwrite_eeg)

# need user input to select out blinks, sacades, heartbeak and muscle artifact
for eegf in eegfs:
    plot_ica(eegf, overwrite=overwrite_eeg)

# this will take even longer ~20+ minutes per subject depending on task length
for eegf in eegfs:
    raw = apply_ica(eegf)
    for event in my_events():
        mark_autoreject(eegf, raw, event, overwrite=overwrite_eeg)
