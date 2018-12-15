# ClassCLI
Command Line Interfaces from class definitions.

[![Build Status](https://travis-ci.org/Hrabal/ClassCLI.svg?branch=master)](https://travis-ci.org/Hrabal/ClassCLI) [![Coverage Status](https://coveralls.io/repos/github/Hrabal/ClassCLI/badge.svg?branch=master)](https://coveralls.io/github/Hrabal/ClassCLI?branch=master)


Very similar to [Fire](https://github.com/google/python-fire), this is a Python module that let you build command line interfaces directly from collection of classes, saving you from writing boilerplate code.

ClassCLI is built on top of argparse, it create arguments of the cli by inspecting the classes in a given list or in a module. Each compatible class is transformed in a first-level argument, each function in a second-level argument, each function's argument in a third level argument.

ClassCLI uses docstrings to build the CLI's help, kwargs defaults to set CLI's pars defaults and type hints to infer CLI's pars types.

ClassCLI can be used to build CLI interfaces on top of existing APIs, or can be used to write scripts with a full-featured CLI writing commands and arguments as classes and functions.

Example code:
```python
from classcli import CliBuilder


class NonCommandClass:
    pass


class MainCommand:
    """Docstring are used for help."""
    callable_cls = True
    command = 'foo'

    def _base(self):
        """Docstring are used for help in methods too."""
        print('This script is running as a foo.')

    def with_args(self,
                  first_arg: int,  # Type annotations are used to add a type check on the CLI arg
                  second_arg):
        print('This script is running as a foo with %s %s.' % (first_arg, second_arg))


class SecondCommand:
    callable_cls = True
    command = 'bar'

    def _base(self):
        print('This script is running in a bar.')

    def order(self,
              order='Beer'  # method kwargs are translated to optiona args in the form of "--arg"
              ):
        print('You ordered a %s' % order)


if __name__ == '__main__':
    CliBuilder(locals()).run_cli()

```


This projects's goals:
 * this project should let fast CLI prototyping
 * this project should stay lightweight
