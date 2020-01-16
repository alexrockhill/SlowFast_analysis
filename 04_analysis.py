from swann.utils import (get_config, get_layout,
                         exclude_subjects)
from swann.analyses import decompose_tfr

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
    decompose_tfr(eegf, overwrite=overwrite)  # defaults to beta
