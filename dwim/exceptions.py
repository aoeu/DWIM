class EmptyCommand(Exception):
    """Raised when empty command passed to `dwim`."""


class NoRuleMatched(Exception):
    """Raised when no rule matched for some command."""
