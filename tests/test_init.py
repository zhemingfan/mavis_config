import pytest
from mavis_config import (
    DEFAULTS,
    get_by_prefix,
    get_library_inputs,
    get_singularity_bindings,
    guess_total_batches,
)

from .util import package_path


@pytest.fixture
def library_input(tmp_path):
    p = tmp_path / "input.txt"

    p.write_text('\n'.join([str(i) for i in range(800)]) + '\n')
    return str(p)


def test_default_matches_json():
    assert DEFAULTS['validate.trans_min_mapping_quality'] == 0


def test_sets_all_defaults():
    assert len(DEFAULTS) == 97


def test_get_by_prefix():
    prefixed = get_by_prefix(DEFAULTS, 'bam_stats.')
    assert len(prefixed) == 4
    assert 'sample_size' in prefixed


class TestGetLibraryInputs:
    def test_no_convert(self, library_input):
        inputs = get_library_inputs(
            {'libraries': {'lib': {'assign': [library_input, library_input]}}}, 'lib'
        )
        assert len(inputs) == 2

    def test_convert(self, library_input):
        inputs = get_library_inputs(
            {
                'libraries': {
                    'lib': {'assign': [library_input, 'conversion_alias']},
                },
                'convert': {'conversion_alias': {'inputs': [library_input]}},
            },
            'lib',
        )
        assert len(inputs) == 2


class TestGuessTotalBatches:
    def test_below_clusters_min(self, library_input):
        batches = guess_total_batches(
            {'cluster.min_clusters_per_file': 900, 'cluster.max_files': 100},
            [library_input],
        )
        assert batches == 1

    def test_above_max_jobs(self, library_input):
        batches = guess_total_batches(
            {'cluster.min_clusters_per_file': 1, 'cluster.max_files': 100},
            [library_input],
        )
        assert batches == 100

    def test_mid_range_jobs(self, library_input):
        batches = guess_total_batches(
            {'cluster.min_clusters_per_file': 100, 'cluster.max_files': 100},
            [library_input],
        )
        assert batches == 8


@pytest.fixture
def bindings(library_input):
    conf = {
        'reference.annotations': ['/annotations/somefile.txt'],
        'reference.reference_genome': ['/reference_genome/somefile.txt'],
        'reference.aligner_reference': ['/aligner_reference/somefile.txt'],
        'reference.masking': ['/masking/somefile.txt'],
        'reference.dgv_annotations': ['/dgv_annotations/somefile.txt'],
        'libraries': {
            'lib': {
                'assign': [
                    library_input,
                    'conversion_alias',
                    '/output_dir/but/yet/another/file.txt',
                ],
                'bam_file': '/bam/file/dir/bam.bam',
            },
        },
        'convert': {'conversion_alias': {'inputs': ['/convert/something.txt']}},
        'output_dir': '/output_dir',
    }
    return get_singularity_bindings(conf)


class TestGetSingularityBindings:
    def test_includes_annotations(self, bindings):
        assert '/annotations:/annotations:ro' in bindings

    def test_includes_masking(self, bindings):
        assert '/masking:/masking:ro' in bindings

    def test_includes_reference_genome(self, bindings):
        assert '/reference_genome:/reference_genome:ro' in bindings

    def test_includes_aligner_reference(self, bindings):
        assert '/aligner_reference:/aligner_reference:ro' in bindings

    def test_includes_conversions(self, bindings):
        assert '/convert:/convert:ro' in bindings

    def test_includes_bam_file(self, bindings):
        assert '/bam/file/dir:/bam/file/dir:ro' in bindings

    def test_includes_library_inputs(self, bindings):
        assert '/reference_genome:/reference_genome:ro' in bindings

    def test_no_ro_output_subdirs(self, bindings):
        assert '/output_dir/but/yet/another:/output_dir/but/yet/another:ro' not in bindings
