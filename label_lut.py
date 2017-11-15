gz4_to_gz2 = {
    'sloan-0.a-0': 't01_smooth_or_features_a01_smooth_count',
    'sloan-0.a-1': 't01_smooth_or_features_a02_features_or_disk_count',
    'sloan-0.a-2': 't01_smooth_or_features_a03_star_or_artifact_count',
    'sloan-1.a-0': 't02_edgeon_a04_yes_count',
    'sloan-1.a-1': 't02_edgeon_a05_no_count',
    'sloan-2.a-0': 't03_bar_a06_bar_count',
    'sloan-2.a-1': 't03_bar_a07_no_bar_count',
    'sloan-3.a-0': 't04_spiral_a08_spiral_count',
    'sloan-3.a-1': 't04_spiral_a09_no_spiral_count',
    'sloan-4.a-0': 't05_bulge_prominence_a10_no_bulge_count',
    'sloan-4.a-1': 't05_bulge_prominence_a11_just_noticeable_count',
    'sloan-4.a-2': 't05_bulge_prominence_a12_obvious_count',
    'sloan-4.a-3': 't05_bulge_prominence_a13_dominant_count',
    'sloan-5.a-0': 't06_odd_a14_yes_count',
    'sloan-5.a-1': 't06_odd_a15_no_count',
    'sloan-7.a-0': 't07_rounded_a16_completely_round_count',
    'sloan-7.a-1': 't07_rounded_a17_in_between_count',
    'sloan-7.a-2': 't07_rounded_a18_cigar_shaped_count',
    'sloan-8.a-0': 't09_bulge_shape_a25_rounded_count',
    'sloan-8.a-1': 't09_bulge_shape_a26_boxy_count',
    'sloan-8.a-2': 't09_bulge_shape_a27_no_bulge_count',
    'sloan-9.a-0': 't10_arms_winding_a28_tight_count',
    'sloan-9.a-1': 't10_arms_winding_a29_medium_count',
    'sloan-9.a-2': 't10_arms_winding_a30_loose_count',
    'sloan-10.a-0': 't11_arms_number_a31_1_count',
    'sloan-10.a-1': 't11_arms_number_a32_2_count',
    'sloan-10.a-2': 't11_arms_number_a33_3_count',
    'sloan-10.a-3': 't11_arms_number_a34_4_count',
    'sloan-10.a-4': 't11_arms_number_a36_more_than_4_count',
    'sloan-10.a-5': 't11_arms_number_a37_cant_tell_count'
}

gz2_to_gz4 = {v: k for k, v in gz4_to_gz2.items()}
