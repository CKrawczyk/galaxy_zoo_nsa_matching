import pandas
import label_lut
from astropy import units as u

matching_radius = 10 * u.arcsec

gz4 = pandas.read_csv('gz4_aggregate_with_metadata_nsa_only_{0}_arcsec.csv'.format(matching_radius.value))
gz2_specz = pandas.read_csv('gz2_specz_nsa_only_{0}_arcsec.csv'.format(matching_radius.value))
gz2_photoz = pandas.read_csv('gz2_photoz_nsa_only_{0}_arcsec.csv'.format(matching_radius.value))
gz2_s82 = pandas.read_csv('gz2_s82_nsa_only_{0}_arcsec.csv'.format(matching_radius.value))

cols_to_match = ['nsa_id', 'survey'] + sorted(list(label_lut.gz4_to_gz2.keys()))
label_lut.gz2_to_gz4['sample'] = 'survey'
gdx = gz4.nsa_id != -999


def rename_to_gz4_and_trim(gz2):
    gz2.columns = [label_lut.gz2_to_gz4[c] if c in label_lut.gz2_to_gz4 else c for c in gz2.columns]
    return gz2[cols_to_match]


gz4_match = gz4[gdx][cols_to_match]
gz2_specz_match = rename_to_gz4_and_trim(gz2_specz)
gz2_photoz_match = rename_to_gz4_and_trim(gz2_photoz)
gz2_s82_match = rename_to_gz4_and_trim(gz2_s82)

gz_all = pandas.concat([gz4_match, gz2_specz_match, gz2_photoz_match, gz2_s82_match], ignore_index=True)
gz_all = gz_all.fillna(value=0)
survey = pandas.DataFrame(gz_all.groupby('nsa_id', as_index=False)['survey'].apply(','.join))
survey.columns = ['survey']
votes = gz_all.groupby('nsa_id', as_index=False).sum()

nsa_reduce = pandas.concat([votes, survey], axis=1)
for col in nsa_reduce.columns:
    if 'sloan-' in col:
        nsa_reduce[col] = nsa_reduce[col].astype(int)

nsa_reduce.to_csv('nsa_all_raw_gz_counts_{0}_arcsec.csv'.format(matching_radius.value), index=False)
