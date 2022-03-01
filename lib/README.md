# a2 lib

In here is are things for the **a2 runtime** to work. There is:

## Autohotkey

A latest **Autohotkey** version to run our scripts.  
And a `lib` underneath for easy access to ALL our built-in Autohotkey scripts.

## cmds

Adhoc `.ahk`-scripts to get data and make use of Autohotkey features without importing them to the runtime. Used by the ui AND a2 modules.

## defaults

A set of templates and default data.

## `*.ahk` scripts

All the backend-a2-runtime scripts are in here.
These are **not** intended for the modules to be used directly and should have kicked of everything one would need from these at runtime startup already.
