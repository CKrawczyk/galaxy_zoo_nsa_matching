from astroquery.sdss import SDSS


def objid_extract(obj_id, full=False):
    masks = {
        'sky_version': 0x7800000000000000,
        'rerun': 0x07FF000000000000,
        'run': 0x0000FFFF00000000,
        'camcol': 0x00000000E0000000,
        'first_field': 0x0000000010000000,
        'field': 0x000000000FFF0000,
        'id': 0x000000000000FFFF
    }
    run = (obj_id & masks['run']) >> 32
    rerun = (obj_id & masks['rerun']) >> 48
    camcol = (obj_id & masks['camcol']) >> 29
    field = (obj_id & masks['field']) >> 16
    id = (obj_id & masks['id']) >> 0
    sky_version = (obj_id & masks['sky_version']) >> 59
    first_field = (obj_id & masks['first_field']) >> 28
    return {
        'run': run,
        'rerun': rerun,
        'camcol': camcol,
        'field': field,
        'id': id,
        'first_field': first_field,
        'sky_version': sky_version
    }


def objid_lookup(obj_id):
    extract = objid_extract(obj_id)
    results = SDSS.query_photoobj(run=extract['run'], camcol=extract['camcol'], field=extract['field'], rerun=extract['rerun'])
    idx = results['objid'] == obj_id
    return results[idx]
