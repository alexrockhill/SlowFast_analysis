from swann.utils import (get_config, get_layout, get_events,
                         exclude_subjects, get_behf, pick_data,
                         my_events, select_events)
from swann.preprocessing import (apply_ica,
                                 mark_autoreject, slowfast2epochs_indices)
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
    all_indices, slow_indices, fast_indices = slowfast2epochs_indices(behf)
    raw = apply_ica(eegf)
    epo_reject_indices = {event: mark_autoreject(eegf, event,
                                                 return_saved=True)
                          for event in my_events()}
    events = get_events(raw, exclude_events=epo_reject_indices)
    raw = pick_data(raw)
    for name, indices in {'All': all_indices, 'Slow': slow_indices,
                          'Fast': fast_indices}.items():
        for event in events:
            my_events = select_events(events[event], indices,
                                      epo_reject_indices[event])
            plot_beta_bursting(eegf, name, event, raw.info,
                               raw.ch_names, my_events,
                               overwrite=overwrite)
            plot_power(eegf, name, event, raw.info,
                       raw.ch_names, my_events,
                       overwrite=overwrite)
