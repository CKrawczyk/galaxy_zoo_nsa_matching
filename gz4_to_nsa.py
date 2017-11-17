from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy import units as u
import pandas
import numpy as np
import progressbar

gz4 = pandas.read_csv('DR8_match_gz4_casjob.csv')
nsa_fits = fits.open('/Volumes/Work/nsa_v1_0_0.fits')
nsa_table = nsa_fits[1].data
matching_radius = 10 * u.arcsec

gz4_c = SkyCoord(ra=np.array(gz4.ra) * u.degree, dec=np.array(gz4.dec) * u.degree)
nsa_c = SkyCoord(ra=nsa_table['RA'] * u.degree, dec=nsa_table['DEC'] * u.degree)
idx, d2d, d3d = gz4_c.match_to_catalog_sky(nsa_c)

cdx = d2d < matching_radius
nsa_ids = np.array([nsa_table.NSAID[i] for i in idx], dtype=float)
nsa_ids[~cdx] = np.nan
nsa_id_match = pandas.concat([gz4, pandas.DataFrame(nsa_ids)], axis=1)
nsa_id_match.columns = ['ra', 'dec', 'objid', 'nsa_id']
nsa_id_match.to_csv('dr8_ra_dec_nsaid_{0}_arcsec.csv'.format(matching_radius.value), index=False)

gz4_all = pandas.read_csv('gz4_aggregate_with_metadata.csv')
sdx = gz4_all['survey'] == 'sloan'
objid = np.array(gz4.objid)

widgets = [
    'Matching: ',
    progressbar.Percentage(),
    ' ', progressbar.Bar(),
    ' ', progressbar.ETA()
]
ct = 0
pbar = progressbar.ProgressBar(widgets=widgets, max_value=sdx.sum())
pbar.start()
for i, row in gz4_all[sdx].iterrows():
    if row.sdss_id in objid:
        mdx = objid == row.sdss_id
        gz4_all.ix[i, 'nsa_id'] = nsa_ids[mdx][0]
    ct += 1
    pbar.update(ct)
pbar.finish()

fdx = np.isfinite(np.array(gz4_all.nsa_id))
gz4_out = gz4_all[fdx]
gz4_out.nsa_id = gz4_out.nsa_id.astype(int)
gz4_out.to_csv('gz4_aggregate_with_metadata_nsa_only_{0}_arcsec.csv'.format(matching_radius.value), index=False)
