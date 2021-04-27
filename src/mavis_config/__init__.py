try:
    # python 3.9 specific
    from collections.abc import Mapping
except ImportError:  # pragma: no cover
    from collections import Mapping  # pragma: no cover

import os
from glob import glob
from typing import Dict, List

from braceexpand import braceexpand
from snakemake.exceptions import WorkflowError
from snakemake.utils import validate as snakemake_validate

from .constants import SUBCOMMAND


def bash_expands(*expressions) -> List[str]:
    """
    expand a file glob expression, allowing bash-style brackets.

    Returns:
        a list of files

    Example:
        >>> bash_expands('./{test,doc}/*py')
        [...]
    """
    result = []
    for expression in expressions:
        eresult = []
        for name in braceexpand(expression):
            for fname in glob(name):
                eresult.append(fname)
        if not eresult:
            raise FileNotFoundError('The expression does not match any files', expression)
        result.extend(eresult)
    return [os.path.abspath(f) for f in result]


class ImmutableDict(Mapping):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


def get_by_prefix(config: Dict, prefix: str) -> Dict:
    return {k.replace(prefix, ''): v for k, v in config.items() if k.startswith(prefix)}


def validate_config(config: Dict, stage: str = SUBCOMMAND.SETUP) -> None:
    """
    Check that the input JSON config conforms to the expected schema as well
    as the other relevant checks such as file exsts
    """
    schema = 'config' if stage != SUBCOMMAND.OVERLAY else 'overlay'

    try:
        snakemake_validate(
            config,
            os.path.join(os.path.dirname(__file__), f'{schema}.json'),
        )
    except Exception as err:
        short_msg = '. '.join(
            [line for line in str(err).split('\n') if line.strip()][:3]
        )  # these can get super long
        raise WorkflowError(short_msg)

    required = []
    if (
        stage not in {SUBCOMMAND.CONVERT, SUBCOMMAND.CLUSTER}
        or stage == SUBCOMMAND.CLUSTER
        and not config['cluster.uninformative_filter']
    ):
        required.append('reference.annotations')

    if stage == SUBCOMMAND.VALIDATE:
        required.extend(['reference.aligner_reference', 'reference.reference_genome'])

    if stage == SUBCOMMAND.SETUP and not config.get('skip_stage.validate'):
        required.append('reference.aligner_reference')

    if (
        stage in {SUBCOMMAND.CLUSTER, SUBCOMMAND.VALIDATE, SUBCOMMAND.ANNOTATE, SUBCOMMAND.SETUP}
        and 'libraries' not in config
    ):
        required.append('libraries')

    for req in required:
        if req not in config:
            raise WorkflowError(f'missing required property: {req}')

    if schema == 'config':
        # check all assignments are conversions aliases or existing files
        for libname, library in config['libraries'].items():
            assignments = []
            for i, assignment in enumerate(library['assign']):
                if assignment in config.get('convert', {}):
                    if 'output_dir' not in config:
                        raise WorkflowError('missing required property: output_dir')
                    # replace the alias with the expected output path
                    converted_output = os.path.join(
                        os.path.join(config['output_dir'], 'converted_outputs'), f'{assignment}.tab'
                    )
                    if stage != SUBCOMMAND.SETUP:
                        assignments.append(converted_output)
                    else:
                        assignments.append(assignment)
                    continue
                try:
                    expanded = bash_expands(assignment)
                    assignments.extend(expanded)
                except FileNotFoundError:
                    raise FileNotFoundError(f'cannot find the expected input file {assignment}')

            library['assign'] = assignments

            if not config.get('skip_stage.validate') and stage in {
                SUBCOMMAND.VALIDATE,
                SUBCOMMAND.SETUP,
            }:
                if not library.get('bam_file', None) or not os.path.exists(library['bam_file']):
                    raise FileNotFoundError(
                        f'missing bam file for library ({libname}), it is a required input when the validate stage is not skipped'
                    )

        # expand and check the input files exist for any conversions
        for conversion in config.get('convert', {}).values():
            expanded = []
            for input_file in conversion['inputs']:
                expanded.extend(bash_expands(input_file))
            conversion['inputs'] = expanded

    # make sure all the reference files specified exist and overload with environment variables where applicable
    for ref_type in list(config.keys()):
        if not ref_type.startswith('reference.'):
            continue
        expanded = []
        for input_file in config[ref_type]:
            expanded.extend(bash_expands(input_file))
        config[ref_type] = expanded


DEFAULTS = {}  # type: ignore
snakemake_validate(
    DEFAULTS,
    os.path.join(os.path.dirname(__file__), 'config.json'),
    set_default=True,
)
DEFAULTS = ImmutableDict(DEFAULTS)  # type: ignore
