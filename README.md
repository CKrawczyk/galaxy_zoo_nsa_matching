# galaxy_zoo_nsa_matching
Code used to match all SDSS galaxy zoo data (from GZ2 up) to the nasa sloan atlas

## aggregate_gz4.py
This script is used to create the aggregated vote counts for all the sloan data in
GZ4 (with metadata).  Update lines 7-10 to point to where the location of the GZ4
data dumps and the subject metadata dump.

It outputs two `csv` files, one without the metadata and one with the metadata.
