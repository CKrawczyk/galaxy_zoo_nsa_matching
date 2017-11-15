# galaxy_zoo_nsa_matching
Code used to match all SDSS galaxy zoo data (from GZ2 up) to the nasa sloan atlas

## aggregate_gz4.py
This script is used to create the aggregated vote counts for all the sloan data in
GZ4 (with metadata).  Update lines 7-10 to point to where the location of the GZ4
data dumps and the subject metadata dump.

It outputs two `csv` files, one without the metadata and one with the metadata.

## ra_dec_lookup.py
This script is used to get the RA and DEC value for the original GZ4 SDSS sample.
The `objid`s are used to look up the positions using an SQL query via `astroquery`.

It outputs one `csv` file that has `objid`, `RA`, and `DEC` for this subsample of GZ4
galaxies.

## gz4_to_nsa.py
This script takes the `RA` and `DEC` matches of the the previous script and does a
6 arcsec match to the NSA catalog.  The resulting `nsa_id` values are added to the
`csv` file output by `aggregate_gz4.py`.  Finally the data table is reduced to only
include data with `nsa_id`s.  Update line 9 to point to where the `nsa_v1_0_0.fits`
file is located.

It outputs two `csv` files, one with `objid`, `RA`, `DEC`, and `nsa_id`, and one with
"nsa only" GZ4 vote counts with metadata.

## gz2_to_nsa.py
This script takes the three GZ2 catalogs (specz, photoz, s82 normal) and does a 6 arcsec
match to the NSA catalog.

It outputs three `csv` files (one for each catalog) that only includes the matched
galaxies with the `nsa_id` column added.

## label_lut.py
This script has a lookup table used to convert the column names of the GZ4 vote count
table to the equivalent columns in the GZ2 data tables (and the other way around).

## gz2_into_gz4_format.py
This final script brings the three GZ2 matched tables into the same format as the GZ4 vote count table and does a final sum of all vote counts based on `nsa_id`.

This outputs one `csv` file with the "all NSA galaxies seen by galaxy zoo ever" raw vote
count catalog.
