# -*- coding: utf-8 -*-

import pytest
from dwim.shells import Powershell


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestPowershell(object):
    @pytest.fixture
    def shell(self):
        return Powershell()

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == '(ls) -and (cd)'

    def test_app_alias(self, shell):
        assert 'function dwim' in shell.app_alias('dwim')
        assert 'function DWIM' in shell.app_alias('DWIM')
        assert 'dwim' in shell.app_alias('dwim')
