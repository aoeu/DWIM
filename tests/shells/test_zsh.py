# -*- coding: utf-8 -*-

import os
import pytest
from dwim.shells.zsh import Zsh


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestZsh(object):
    @pytest.fixture
    def shell(self):
        return Zsh()

    @pytest.fixture(autouse=True)
    def shell_aliases(self):
        os.environ['TF_SHELL_ALIASES'] = (
            'dwim=\'eval $(dwim $(fc -ln -1 | tail -n 1))\'\n'
            'l=\'ls -CF\'\n'
            'la=\'ls -A\'\n'
            'll=\'ls -alF\'')

    @pytest.mark.parametrize('before, after', [
        ('dwim', 'eval $(dwim $(fc -ln -1 | tail -n 1))'),
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {
            'dwim': 'eval $(dwim $(fc -ln -1 | tail -n 1))',
            'l': 'ls -CF',
            'la': 'ls -A',
            'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias dwim' in shell.app_alias('dwim')
        assert 'alias DWIM' in shell.app_alias('DWIM')
        assert 'dwim' in shell.app_alias('dwim')
        assert 'PYTHONIOENCODING' in shell.app_alias('dwim')

    def test_app_alias_variables_correctly_set(self, shell):
        alias = shell.app_alias('dwim')
        assert "alias dwim='TF_CMD=$(TF_ALIAS" in alias
        assert '$(TF_ALIAS=dwim PYTHONIOENCODING' in alias
        assert 'PYTHONIOENCODING=utf-8 TF_SHELL_ALIASES' in alias
        assert 'ALIASES=$(alias) dwim' in alias

    def test_get_history(self, history_lines, shell):
        history_lines([': 1432613911:0;ls', ': 1432613916:0;rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
