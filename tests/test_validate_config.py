import os

import pytest
from mavis_config import validate_config
from snakemake.exceptions import WorkflowError

from .util import not_raises, package_path

EXISTING_FILE = package_path('src/mavis_config/overlay.json')


class TestOverlayConfig:
    def test_error_on_missing_required(self):
        with pytest.raises(WorkflowError):
            validate_config({}, stage='overlay')

    def test_ok_with_required(self):
        with not_raises(WorkflowError):
            validate_config(
                {'reference.annotations': [EXISTING_FILE]},
                stage='overlay',
            )


class TestSetup:
    def test_error_on_missing_aligner_reference(self):
        with pytest.raises(WorkflowError) as err:
            validate_config({'reference.annotations': [EXISTING_FILE]}, stage='setup')
        assert 'missing required property: reference.aligner_reference' in str(err)

    def test_error_on_missing_libraries(self):
        with pytest.raises(WorkflowError) as err:
            validate_config(
                {
                    'reference.annotations': [EXISTING_FILE],
                    'reference.aligner_reference': [EXISTING_FILE],
                    'reference.reference_genome': [EXISTING_FILE],
                },
                stage='setup',
            )
        assert 'missing required property: libraries' in str(err)

    def test_library_missing_disease_status(self):
        with pytest.raises(WorkflowError) as err:
            conf = validate_config(
                {
                    'reference.annotations': [EXISTING_FILE],
                    'skip_stage.validate': True,
                    'reference.reference_genome': [EXISTING_FILE],
                    'libraries': {'AAAA': {'protocol': 'genome'}},
                },
                stage='setup',
            )
        assert 'ValidationError: \'disease_status\' is a required property' in str(err)

    def test_library_missing_protocol(self):
        with pytest.raises(WorkflowError) as err:
            conf = validate_config(
                {
                    'reference.annotations': [EXISTING_FILE],
                    'skip_stage.validate': True,
                    'reference.reference_genome': [EXISTING_FILE],
                    'libraries': {'AAAA': {'disease_status': 'diseased'}},
                },
                stage='setup',
            )
        assert 'ValidationError: \'protocol\' is a required property' in str(err)

    def test_library_missing_assign(self):
        with pytest.raises(WorkflowError) as err:
            conf = validate_config(
                {
                    'reference.annotations': [EXISTING_FILE],
                    'skip_stage.validate': True,
                    'reference.reference_genome': [EXISTING_FILE],
                    'libraries': {'AAAA': {'disease_status': 'diseased', 'protocol': 'genome'}},
                },
                stage='setup',
            )
        assert 'ValidationError: \'assign\' is a required property' in str(err)

    def test_expanding_input_files(self):
        overlay = os.path.abspath(package_path('src/mavis_config/overlay.json'))
        main = os.path.abspath(package_path('src/mavis_config/config.json'))
        conf = {
            'reference.annotations': [EXISTING_FILE],
            'skip_stage.validate': True,
            'reference.reference_genome': [EXISTING_FILE],
            'libraries': {
                'AAAA': {
                    'disease_status': 'diseased',
                    'protocol': 'genome',
                    'assign': [package_path('src/mavis_config/*.json')],
                }
            },
        }
        validate_config(
            conf,
            stage='setup',
        )
        assert conf['libraries']['AAAA']['assign'] == [main, overlay]

    def test_missing_output_dir_for_convert(self):
        with pytest.raises(WorkflowError) as err:
            conf = {
                'reference.annotations': [EXISTING_FILE],
                'skip_stage.validate': True,
                'reference.reference_genome': [EXISTING_FILE],
                'libraries': {
                    'AAAA': {
                        'disease_status': 'diseased',
                        'protocol': 'genome',
                        'assign': ['dlly'],
                    }
                },
                'convert': {
                    'dlly': {
                        'file_type': 'delly',
                        'inputs': [package_path('src/mavis_config/*.json')],
                    }
                },
            }
            validate_config(
                conf,
                stage='setup',
            )
        assert 'missing required property: output_dir' in str(err)

    def test_expanding_convert_inputs(self):
        overlay = os.path.abspath(package_path('src/mavis_config/overlay.json'))
        main = os.path.abspath(package_path('src/mavis_config/config.json'))
        conf = {
            'reference.annotations': [EXISTING_FILE],
            'skip_stage.validate': True,
            'reference.reference_genome': [EXISTING_FILE],
            'libraries': {
                'AAAA': {
                    'disease_status': 'diseased',
                    'protocol': 'genome',
                    'assign': ['dlly'],
                }
            },
            'convert': {
                'dlly': {
                    'file_type': 'delly',
                    'inputs': [package_path('src/mavis_config/*.json')],
                }
            },
            'output_dir': '.',
        }
        validate_config(
            conf,
            stage='setup',
        )
        assert conf['libraries']['AAAA']['assign'] == ['dlly']
        assert conf['convert']['dlly']['inputs'] == [main, overlay]
