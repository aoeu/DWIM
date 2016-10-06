# -*- coding: utf-8 -*-

import pytest
from dwim.shells import Fish


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('dwim.shells.fish.Popen')
        mock.return_value.stdout.read.return_value = (
            b'cd\nfish_config\ndwim\nfunced\nfuncsave\ngrep\nhistory\nll\nls\n'
            b'man\nmath\npopd\npushd\nruby')
        return mock

    @pytest.fixture
    def os_environ(self, monkeypatch, key, value):
        monkeypatch.setattr('os.environ', {key: value})

    @pytest.mark.parametrize('key, value', [
        ('TF_OVERRIDDEN_ALIASES', 'cut,git,sed'),  # legacy
        ('DWIM_OVERRIDDEN_ALIASES', 'cut,git,sed'),
        ('DWIM_OVERRIDDEN_ALIASES', 'cut, git, sed'),
        ('DWIM_OVERRIDDEN_ALIASES', ' cut,\tgit,sed\n'),
        ('DWIM_OVERRIDDEN_ALIASES', '\ncut,\n\ngit,\tsed\r')])
    def test_get_overridden_aliases(self, shell, os_environ):
        assert shell._get_overridden_aliases() == {'cd', 'cut', 'git', 'grep',
                                                   'ls', 'man', 'open', 'sed'}

    @pytest.mark.parametrize('before, after', [
        ('cd', 'cd'),
        ('pwd', 'pwd'),
        ('dwim', 'fish -ic "dwim"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('grep', 'grep'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('man', 'man'),
        ('open', 'open'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"'),
        ('ls', 'ls')])  # Fish has no aliases but functions
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'dwim': 'dwim',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math',
                                       'popd': 'popd',
                                       'pushd': 'pushd',
                                       'ruby': 'ruby'}

    def test_app_alias(self, shell):
        assert 'function dwim' in shell.app_alias('dwim')
        assert 'function DWIM' in shell.app_alias('DWIM')
        assert 'dwim' in shell.app_alias('dwim')
        assert 'TF_ALIAS=dwim PYTHONIOENCODING' in shell.app_alias('dwim')
        assert 'PYTHONIOENCODING=utf-8 dwim' in shell.app_alias('dwim')

    def test_app_alias_alter_history(self, settings, shell):
        settings.alter_history = True
        assert 'history --delete' in shell.app_alias('DWIM')
        assert 'history --merge' in shell.app_alias('DWIM')
        settings.alter_history = False
        assert 'history --delete' not in shell.app_alias('DWIM')
        assert 'history --merge' not in shell.app_alias('DWIM')

    def test_get_history(self, history_lines, shell):
        history_lines(['- cmd: ls', '  when: 1432613911',
                       '- cmd: rm', '  when: 1432613916'])
        assert list(shell.get_history()) == ['ls', 'rm']

    @pytest.mark.parametrize('entry, entry_utf8', [
        ('ls', '- cmd: ls\n   when: 1430707243\n'),
        (u'echo café', '- cmd: echo café\n   when: 1430707243\n')])
    def test_put_to_history(self, entry, entry_utf8, builtins_open, mocker, shell):
        mocker.patch('dwim.shells.fish.time', return_value=1430707243.3517463)
        shell.put_to_history(entry)
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(entry_utf8)
