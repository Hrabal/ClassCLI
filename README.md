# ClassCLI
Command Line Interfaces from class definitione

Very similar to [Fire](https://github.com/google/python-fire), this is a Python module that let you build command line interfaces directly from classes, without having to deal with argument definitions.

ClassCLI is built on top of argparse, it create arguments of the cli by inspecting the classes in a module. Each compatible class is transformed in a first-level argument, each function in a second-level argument, each function's argument in a third level argument.

ClassCLI uses docstrings to build the CLI's help, kwargs defaults to set CLI's pars defaults and type hints to infer CLI's pars types.

