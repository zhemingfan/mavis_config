from mavis_config import DEFAULTS, get_by_prefix


def test_default_matches_json():
    assert DEFAULTS['validate.trans_min_mapping_quality'] == 0


def test_sets_all_defaults():
    assert len(DEFAULTS) == 97


def test_get_by_prefix():
    prefixed = get_by_prefix(DEFAULTS, 'bam_stats.')
    assert len(prefixed) == 4
    assert 'sample_size' in prefixed
