# -*- encoding: utf-8 -*-


class _GenConst(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return u'<const: {}>'.format(self._name)


KEY_UP = _GenConst('↑')
KEY_DOWN = _GenConst('↓')
KEY_CTRL_C = _GenConst('Ctrl+C')

ACTION_SELECT = _GenConst('select')
ACTION_ABORT = _GenConst('abort')
ACTION_PREVIOUS = _GenConst('previous')
ACTION_NEXT = _GenConst('next')

ALL_ENABLED = _GenConst('All rules enabled')
DEFAULT_RULES = [ALL_ENABLED]
DEFAULT_PRIORITY = 1000

DEFAULT_SETTINGS = {'rules': DEFAULT_RULES,
                    'exclude_rules': [],
                    'wait_command': 3,
                    'require_confirmation': True,
                    'no_colors': False,
                    'debug': False,
                    'priority': {},
                    'history_limit': None,
                    'alter_history': True,
                    'wait_slow_command': 15,
                    'slow_commands': ['lein', 'react-native', 'gradle',
                                      './gradlew'],
                    'env': {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'}}

ENV_TO_ATTR = {'DWIM_RULES': 'rules',
               'DWIM_EXCLUDE_RULES': 'exclude_rules',
               'DWIM_WAIT_COMMAND': 'wait_command',
               'DWIM_REQUIRE_CONFIRMATION': 'require_confirmation',
               'DWIM_NO_COLORS': 'no_colors',
               'DWIM_DEBUG': 'debug',
               'DWIM_PRIORITY': 'priority',
               'DWIM_HISTORY_LIMIT': 'history_limit',
               'DWIM_ALTER_HISTORY': 'alter_history',
               'DWIM_WAIT_SLOW_COMMAND': 'wait_slow_command',
               'DWIM_SLOW_COMMANDS': 'slow_commands'}

SETTINGS_HEADER = u"""# DWIM settings file
#
# The rules are defined as in the example bellow:
#
# rules = ['cd_parent', 'git_push', 'python_command', 'sudo']
#
# The default values are as follows. Uncomment and change to fit your needs.
# See https://github.com/nvbn/dwim#settings for more information.
#

"""
