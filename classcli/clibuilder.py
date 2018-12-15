# -*- coding: utf-8 -*-
"""
Command line factory
"""
import sys
import argparse
import inspect

try:
    from sty import fg, rs
except ImportError:
    class EmptyStringer:
        def __getattribute__(self, attr):
            return ''
    fg = rs = EmptyStringer()


def _load_object(module_or_obj_collection):
    # Input cleanup, get an iterable of classes out of the argument
    if isinstance(module_or_obj_collection, dict):
        iterator = ((cname, obj) for cname, obj in module_or_obj_collection.items() if inspect.isclass(obj))
    elif isinstance(module_or_obj_collection, list):
        iterator = ((obj.__name__, obj) for obj in module_or_obj_collection if inspect.isclass(obj))
    elif inspect.ismodule(module_or_obj_collection):
        iterator = inspect.getmembers(module_or_obj_collection, inspect.isclass)
    else:
        raise TypeError('Unsupported type for CLI init: list/dist with classes in it or module supported.')
    return iterator


def _make_bool_arg(arg):
    return ('-%s' % arg.name, ), {'action': 'store_false' if arg.default is False else 'store_true'}


def _make_arg(arg, used_aliases: set):
    arg_kwargs = {
        'type': arg.annotation if arg.annotation is not arg.empty else str
    }
    if arg.default is not arg.empty:
        arg_kwargs['default'] = arg.default
        names = ['--%s' % arg.name, ]
        try:
            letter = next(l for l in arg.name if l not in used_aliases)
            names.insert(0, '-%s' % letter)
            used_aliases.add(letter)
        except StopIteration:
            raise argparse.ArgumentError(None, 'Impossible to find an alias for argument %s.' % arg)
    else:
        names = (arg.name, )
    return names, arg_kwargs


def _read_arguments(self, method_args_parser, fnc):
    used_aliases = set()
    for arg in inspect.signature(fnc).parameters.values():
        arg_kwargs = {}
        if arg.annotation is bool:
            names, arg_kwargs = _make_bool_arg(arg)
        else:
            names, arg_kwargs = _make_arg(arg, used_aliases)
        method_args_parser.add_argument(*names, **arg_kwargs)


class ClassParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('%serror: %s%s\n' % (fg.red, message, rs.fg))
        self.print_help()
        sys.exit(2)


class CliBuilder:

    def __init__(self, module_or_obj_collection):
        """ Creates a hierarchical parser from a module, a list or a dict.
        Filters the input looking for classes, and only uses those who have bool(callable_cls) == True
        """
        # Main argparse instance
        self.parser = ClassParser()
        # subparser collector
        self.subparsers = self.parser.add_subparsers()

        # For every controller class defined in the input module we add a subparser
        for _, cls in _load_object(module_or_obj_collection):
            # Only classes with callable_cls will be added as subparser (so to exclude utility classes)
            if getattr(cls, 'callable_cls', False):
                self._make_subparser(cls)

    def _make_subparser(self, cls):
        # Help for this command from the class docstring and the _base method docstring
        help_str = '\n'.join(doc for doc in (inspect.getdoc(cls), inspect.getdoc(cls._base)) if doc)

        # Instance of the controller class that will be called
        controller = cls()

        # Bind the subparser to the command defined in the class, to run the _base method
        cls_parser = self.subparsers.add_parser(controller.command, help=help_str)
        cls_parser.set_defaults(func=controller._base)

        # Every method in the controller class will have it's own subparser
        method_parser = cls_parser.add_subparsers()
        for _, fnc in inspect.getmembers(controller, inspect.ismethod):
            # Exclude the 'private' methods only methods with no leading underscore are used
            if not fnc.__name__.startswith('_'):
                # Make a new subparser in the class one
                method_args_parser = method_parser.add_parser(fnc.__name__, help=inspect.getdoc(fnc) or '')
                # Bind the class method to the subparser argument
                method_args_parser.set_defaults(func=fnc)
                self._read_arguments(method_args_parser, fnc)

    def run_cli(self, args=None):
        if args:
            args = map(str, args)
        args = self.parser.parse_args(args or sys.argv[1:])
        try:
            if not vars(args):
                raise argparse.ArgumentError(None, 'At least one argument needed.')
            return args.func(**{k: v for k, v in vars(args).items() if k != 'func'})
        except argparse.ArgumentError as ex:
            print('%sERROR! Wrong command invocation: %s%s' % (fg.red, ex.message, rs.fg))
            print('Please read the help:')
            self.parser.print_help()
