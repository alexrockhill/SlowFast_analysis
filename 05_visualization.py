import numpy as np

from swann.utils import (get_config, get_layout, get_events,
                         exclude_subjects, get_behf, pick_data,
                         my_events, select_events)
from swann.preprocessing import (apply_ica,
                                 mark_autoreject, slowfast2epochs_indices)
from swann.viz import (plot_bursting, plot_power, plot_spectrogram,
                       plot_group_bursting, plot_group_power,
                       plot_burst_shape)

config = get_config()
layout = get_layout()

eegfs = (layout.get(task=config['task'],
                    suffix='eeg', extension='bdf') +
         layout.get(task=config['task'],
                    suffix='eeg', extension='vmrk'))
eegfs = exclude_subjects(eegfs)

overwrite = \
    input('Overwrite plots if they exist? (y/n)\n').upper() == 'Y'

np.random.seed(config['seed'])

# loop across subjects
infos = list()
these_events_all = dict()
for eegf in eegfs:
    behf = get_behf(eegf)
    all_indices, slow_indices, fast_indices = slowfast2epochs_indices(behf)
    raw = apply_ica(eegf)
    epo_reject_indices = {event: mark_autoreject(eegf, event,
                                                 return_saved=True)
                          for event in my_events()}
    events = get_events(raw, exclude_events=epo_reject_indices)
    raw = pick_data(raw)
    infos.append(raw.info)
    these_events_all[eegf.path] = dict()
    for event in events:
        indices = np.random.choice(range(events[event].shape[0]), 10)
        these_events = select_events(events[event], indices,
                                     epo_reject_indices[event])
        plot_spectrogram(eegf, raw, event, these_events, overwrite=overwrite)
    for name, indices in {'All': all_indices, 'Slow': slow_indices,
                          'Fast': fast_indices}.items():
        these_events_all[eegf.path][name] = dict()
        for event in events:
            these_events = select_events(events[event], indices,
                                         epo_reject_indices[event])
            these_events_all[eegf.path][name][event] = these_events
            plot_bursting(eegf, name, event, raw.info,
                          these_events, overwrite=overwrite)
            plot_bursting(eegf, name, event, raw.info, these_events,
                          picks=['C3', 'C4'], overwrite=overwrite)
            plot_power(eegf, name, event, raw.info,
                       these_events, overwrite=overwrite)
            plot_power(eegf, name, event, raw.info,
                       these_events, picks=['C3', 'C4'], overwrite=overwrite)
            plot_burst_shape(eegf, name, event, raw.info,
                             these_events, overwrite=overwrite)

for name, indices in {'All': all_indices, 'Slow': slow_indices,
                      'Fast': fast_indices}.items():
    for event in events:
        plot_group_bursting(eegfs, name, event, infos,
                            these_events_all, overwrite=overwrite)
        plot_group_bursting(eegf, name, event, infos, these_events_all,
                            picks=['C3', 'C4'], overwrite=overwrite)
        plot_group_power(eegfs, name, event, infos,
                         these_events_all, overwrite=overwrite)
        plot_group_power(eegfs, name, event, infos,
                         these_events_all, picks=['C3', 'C4'],
                         overwrite=overwrite)
