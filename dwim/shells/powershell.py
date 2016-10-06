from .generic import Generic


class Powershell(Generic):
    def app_alias(self, dwim):
        return 'function ' + dwim + ' { \n' \
               '    $dwim = $(dwim (Get-History -Count 1).CommandLine);\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($dwim)) {\n' \
               '        if ($dwim.StartsWith("echo")) { $dwim = $dwim.Substring(5); }\n' \
               '        else { iex "$dwim"; }\n' \
               '    }\n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return 'iex "dwim --alias"', '$profile'
