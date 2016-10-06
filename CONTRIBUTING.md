# Report issues
If you have any issue with DWIM, sorry about that, but we will do what we
can to fix that. Actually, maybe we already have, so first thing to do is to
update DWIM and see if the bug is still there.

If it is (sorry again), check if the problem has not already been reported and
if not, just open an issue on [GitHub](https://github.com/aoeu/dwim) with
the following basic information:
  - the output of `dwim --version` (something like `DWIM 3.1 using
    Python 3.5.0`);
  - your shell and its version (`bash`, `zsh`, *Windows PowerShell*, etc.);
  - your system (Debian 7, ArchLinux, Windows, etc.);
  - how to reproduce the bug;
  - the output of DWIM with `DWIM_DEBUG=true` exported (typically execute
    `export DWIM_DEBUG=true` in your shell before DWIM);
  - if the bug only appears with a specific application, the output of that
    application and its version;
  - anything else you think is relevant.

It's only with enough information that we can do something to fix the problem.

# Make a pull request
We gladly accept pull request on the [official
repository](https://github.com/aoeu/dwim) for new rules, new features, bug
fixes, etc.
