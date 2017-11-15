from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io import fits
from astropy.io import ascii
from astropy.table import MaskedColumn
import numpy as np

nsa_fits = fits.open('/Volumes/Work/nsa_v1_0_0.fits')
nsa_table = nsa_fits[1].data
nsa_c = SkyCoord(ra=nsa_table['RA'] * u.degree, dec=nsa_table['DEC'] * u.degree)

gz2_specz = ascii.read('../GZ_data_dumps/zoo2MainSpecz.csv')
gz2_photoz = ascii.read('../GZ_data_dumps/zoo2MainPhotoz.csv')
gz2_s82 = ascii.read('../GZ_data_dumps/zoo2Stripe82Normal.csv')


def cross_match(gz2, cone=6 * u.arcsec):
    gz2_c = SkyCoord(ra=gz2['ra'] * u.degree, dec=gz2['dec'] * u.degree)
    idx, d2d, d3d = gz2_c.match_to_catalog_sky(nsa_c)
    cdx = d2d > cone
    nsa_ids = np.array([nsa_table.NSAID[i] for i in idx])
    nsa_column = MaskedColumn(nsa_ids, name='nsa_id', mask=cdx)
    gz2.add_column(nsa_column)
    return ~cdx


print('match NSA to spacz')
ndx = cross_match(gz2_specz)
gz2_specz[ndx].write('gz2_specz_nsa_only.csv', format='ascii.csv', overwrite=True)

print('match NSA to photoz')
ndx = cross_match(gz2_photoz)
gz2_photoz[ndx].write('gz2_photoz_nsa_only.csv', format='ascii.csv', overwrite=True)

print('match NSA to s82')
ndx = cross_match(gz2_s82)
gz2_s82[ndx].write('gz2_s82_nsa_only.csv', format='ascii.csv', overwrite=True)
