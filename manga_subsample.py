from astropy.io import fits
from astropy.table import Table
from astropy import units as u
import pandas

matching_radius = 10 * u.arcsec

manga_fits = fits.open('MaNGA_targets_extNSA_tiled.fits')
manga_table = Table(manga_fits[1].data)

gz = pandas.read_csv('nsa_all_raw_gz_counts_{0}_arcsec.csv'.format(matching_radius.value))
gdx = (manga_table['IFUDESIGNSIZE'] > 0) & (manga_table['BADPHOTFLAG'] == 0)

match_table = manga_table[gdx]['MANGAID', 'IFUDESIGNSIZE', 'IFU_RA', 'IFU_DEC', 'IAUNAME', 'NSAID', 'OBJECT_RA', 'OBJECT_DEC', 'MANGA_TILEID']
match_table = match_table.to_pandas()
match_table.columns = ['MANGAID', 'IFUDESIGNSIZE', 'IFU_RA', 'IFU_DEC', 'IAUNAME', 'nsa_id', 'OBJECT_RA', 'OBJECT_DEC', 'MANGA_TILEID']

join_table = match_table.join(gz.set_index('nsa_id'), on='nsa_id')
join_table.to_csv('MaNGA_all_raw_gz_counts_{0}_arcsec.csv'.format(matching_radius.value), index=False)
bdx = join_table['sloan-9.a-2'].isnull()
print('Missing galaxies: {0}'.format(bdx.sum()))
if bdx.any():
    pandas.DataFrame(join_table[bdx]['MANGAID'], columns=['MANGAID']).to_csv('bad_ids_{0}_arcsec.csv'.format(matching_radius.value), index=False)
