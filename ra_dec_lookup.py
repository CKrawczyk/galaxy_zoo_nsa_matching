from astroquery.sdss import SDSS
from astropy.table import vstack
import progressbar
import pandas

cmd = 'SELECT DISTINCT p.ra, p.dec, p.objid FROM PhotoObjAll AS p   WHERE p.objid in {0}'

widgets = [
    'Fetching: ',
    progressbar.Percentage(),
    ' ', progressbar.Bar(),
    ' ', progressbar.ETA()
]


def many_objid_lookup(obj_ids, chunk_size=300):
    ids_chunks = [obj_ids[i:i + chunk_size] for i in range(0, len(obj_ids), chunk_size)]
    table = []
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=len(ids_chunks))
    pbar.start()
    for idx, ids in enumerate(ids_chunks):
        table.append(SDSS.query_sql(cmd.format(tuple(ids))))
        pbar.update(idx+1)
    pbar.finish()
    return vstack(table)


gz4 = pandas.read_csv('gz4_aggregate_with_metadata.csv')
fdx = ~pandas.isnull(gz4.sdss_id)
dr8ids = pandas.np.array(gz4['sdss_id'][fdx]).astype(int).tolist()
ra_dec_table = many_objid_lookup(dr8ids)
ra_dec_table.write('dr8_ra_dec.csv', format='ascii.csv')
