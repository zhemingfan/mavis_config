import pytest
from mavis_config.constants import SUBCOMMAND

from .util import not_raises


class TestMavisNamespace:
    def test_enforce_error(self):
        with pytest.raises(KeyError):
            SUBCOMMAND.enforce('k')

    def test_enforce_ok(self):
        with not_raises(KeyError):
            SUBCOMMAND.enforce('setup')

    def test_to_dict(self):
        assert len(SUBCOMMAND.to_dict()) == 8

    def test_keys(self):
        assert len(SUBCOMMAND.keys()) == 8

    def test_in(self):
        assert 'setup' in SUBCOMMAND

    def test_getitem(self):
        assert SUBCOMMAND['SETUP'] == 'setup'

    def test_error_bad_index(self):
        with pytest.raises(KeyError):
            SUBCOMMAND['setup']

    def test_iterate(self):
        assert len(SUBCOMMAND) == 8

    def test_reverse(self):
        assert SUBCOMMAND.reverse('setup') == 'SETUP'

    def test_reverse_error(self):
        with pytest.raises(KeyError):
            SUBCOMMAND.reverse('SETUP')
