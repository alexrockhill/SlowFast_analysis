from swann.utils import (get_config, get_layout,
                         exclude_subjects)
from swann.preprocessing import apply_ica
from swann.analyses import decompose_tfr, find_bursts

config = get_config()
layout = get_layout()

eegfs = (layout.get(task=config['task'],
                    suffix='eeg', extension='bdf') +
         layout.get(task=config['task'],
                    suffix='eeg', extension='vmrk'))
eegfs = exclude_subjects(eegfs)

overwrite = \
    input('Overwrite analysis data if ' +
          'they exist? (y/n)\n').upper() == 'Y'

# loop across subjects: may take ~10 minutes each
for eegf in eegfs:
    raw = apply_ica(eegf)
    decompose_tfr(eegf, raw, overwrite=overwrite)  # defaults to beta

for eegf in eegfs:
    tfr, ch_names, sfreq = decompose_tfr(eegf, return_saved=True)
    find_bursts(eegf, tfr, ch_names, overwrite=overwrite)
