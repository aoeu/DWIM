# -*- coding: utf-8 -*-

import pytest
from dwim.shells.tcsh import Tcsh


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestTcsh(object):
    @pytest.fixture
    def shell(self):
        return Tcsh()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('dwim.shells.tcsh.Popen')
        mock.return_value.stdout.read.return_value = (
            b'dwim\teval $(dwim $(fc -ln -1))\n'
            b'l\tls -CF\n'
            b'la\tls -A\n'
            b'll\tls -alF')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('dwim', 'eval $(dwim $(fc -ln -1))'),
        ('awk', 'awk'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'dwim': 'eval $(dwim $(fc -ln -1))',
                                       'l': 'ls -CF',
                                       'la': 'ls -A',
                                       'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias dwim' in shell.app_alias('dwim')
        assert 'alias DWIM' in shell.app_alias('DWIM')
        assert 'dwim' in shell.app_alias('dwim')

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
