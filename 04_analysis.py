from swann.utils import (get_config, get_layout, get_behf,
                         exclude_subjects, my_events, get_events)
from swann.preprocessing import (apply_ica, mark_autoreject,
                                 slowfast2epochs_indices)

config = get_config()
layout = get_layout()

eegfs = layout.get(task=config['task'],
                   suffix='eeg', extension='bdf')
eegfs = exclude_subjects(eegfs)

overwrite = \
    input('Overwrite analysis data if '
          'they exist? (y/n)\n').upper() == 'Y'

these_events_all = {event: {name: dict() for name in ['All', 'Slow', 'Fast']}
                    for event in my_events()}
for eegf in eegfs:
    behf = get_behf(eegf)
    all_indices, slow_indices, fast_indices = slowfast2epochs_indices(behf)
    raw = apply_ica(eegf)
    epo_reject_indices = {event: mark_autoreject(eegf, event,
                                                 return_saved=True)
                          for event in my_events()}
    events = get_events(raw, exclude_events=epo_reject_indices)
