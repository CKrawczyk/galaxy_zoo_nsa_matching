import pandas
from collections import Counter, OrderedDict
from pandas.io.json.normalize import nested_to_record
import progressbar
import json

missing_manga_data = pandas.read_csv('../GZ_data_dumps/2017-10-29_galaxy_zoo_missing_manga_classifications.csv')
sdss_lost_data = pandas.read_csv('../GZ_data_dumps/2017-10-29_galaxy_zoo_sdss_lost_set_classifications.csv')
sdss_data = pandas.read_csv('../GZ_data_dumps/2017-10-29_galaxy_zoo_sloan_classifications.csv')
subject_data = pandas.read_csv('../GZ_data_dumps/galaxy_zoo_subjects.csv')
subject_data['subject_id'] = [s[9:-1] for s in subject_data._id]

keys = [
    'sloan-0',
    'sloan-1',
    'sloan-2',
    'sloan-3',
    'sloan-4',
    'sloan-5',
    'sloan-7',
    'sloan-8',
    'sloan-9',
    'sloan-10'
]

output = OrderedDict([
    ('subject_id', [])
])

for k in keys:
    output[k] = []


def counter_without_nan(group, key):
    c = Counter(group[key])
    if pandas.np.nan in c:
        c.pop(pandas.np.nan)
    return OrderedDict(sorted(c.items()))


widgets = [
    'Reducing: ',
    progressbar.Percentage(),
    ' ', progressbar.Bar(),
    ' ', progressbar.ETA()
]


def aggregate(data):
    ct = 0
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(data.subject_id.unique()))
    pbar.start()
    for name, group in data.groupby(data.subject_id):
        output['subject_id'].append(name)
        for k in keys:
            output[k].append(counter_without_nan(group, k))
        ct += 1
        pbar.update(ct)
    pbar.finish()


print('missing manga')
aggregate(missing_manga_data)

print('lost set')
aggregate(sdss_lost_data)

print('sdss')
aggregate(sdss_data)

subject_id = pandas.DataFrame(output['subject_id'])
subject_id.columns = ['subject_id']
flat_output = [subject_id]
for k in keys:
    flat_keys = pandas.DataFrame(nested_to_record(output[k]))
    flat_keys.columns = ['{0}.{1}'.format(k, i) for i in flat_keys.columns.values]
    flat_output.append(flat_keys)

vote_counts = pandas.concat(flat_output, axis=1)
vote_counts.to_csv('gz4_aggregate_with_subject_id.csv', index=False)

join_table = vote_counts.set_index('subject_id').join(subject_data.set_index('subject_id'))
join_table.index = pandas.RangeIndex(len(join_table.index))


def json_or_nan(s):
    if isinstance(s, str):
        return json.loads(s)
    else:
        return {}


metadata = join_table.metadata.apply(json_or_nan)
metadata_table = pandas.DataFrame(nested_to_record(metadata))
del join_table['metadata']
pandas.concat([join_table, metadata_table], axis=1).to_csv('gz4_aggregate_with_metadata.csv', index=False)
