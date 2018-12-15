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
