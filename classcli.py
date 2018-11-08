# -*- coding: utf-8 -*-
"""
Command line interface factory
"""
import argparse
import inspect


try:
    # If sty is installed we use colors
    from sty import fg, rs
except ImportError:
    # If not, we add empty spaces instead of colors
    class AlwaysEmptyString:
        def __getattr__(self, k):
            return ''
    fg = rs = AlwaysEmptyString()


class CliBuilder:
    def __init__(self, controllers_module):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers()

        # For every controller class defined in the controllers_module module we add a subparser
        for _, cls in inspect.getmembers(controllers_module, inspect.isclass):
            # Only classes with _callable will be added as subparser (so to exclude utility classes)
            if getattr(cls, 'callable_cls', False):
                # Instantiate the controller class
                controller = cls()
                # Bind the subparser to the command defined in the class
                cls_parser = subparsers.add_parser(controller.command, help=cls.__doc__)
                cls_parser.set_defaults(func=controller._base)
                # Every method in the controller class will have it's own subparser
                method_parser = cls_parser.add_subparsers()
                for _, fnc in inspect.getmembers(controller, inspect.ismethod):
                    if fnc.__name__ not in ('__init__', '_base'):
                        method = method_parser.add_parser(fnc.__name__, help=fnc.__doc__)
                        # Bind the class method to the subparser argument
                        method.set_defaults(func=fnc)
                        for arg in inspect.signature(fnc).parameters.values():
                            name = f'--{arg.name}' if arg.default is not arg.empty else arg.name
                            default = arg.default if arg.default is not arg.empty else None
                            method.add_argument(name,
                                                type=arg.annotation or str,
                                                default=default
                                                )

    def run_cli(self):
        args = self.parser.parse_args()
        try:
            if not vars(args):
                raise AttributeError
            args.func(**{k: v for k, v in vars(args).items() if k != 'func'})
        except AttributeError:
            import traceback
            print(f'{fg.red}ERROR! Wrong command invocation, plese read the help:')
            print(f'Base usage:{rs.fg}')
            self.parser.print_help()
            # retrieve subparsers from parser
            subparsers_actions = [
                action for action in self.parser._actions
                if isinstance(action, argparse._SubParsersAction)]
            # there will probably only be one subparser_action,
            # but better save than sorry
            for subparsers_action in subparsers_actions:
                # get all subparsers and print help
                for choice, subparser in subparsers_action.choices.items():
                    print(f"\nCommand {fg.red}'{choice}'{rs.fg}")
                    print(subparser.format_help())
