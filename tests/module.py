class TestClass:
        callable_cls = True
        command = 'test'

        def _base(self):
            return 1

        def test_method(self):
            return 2

        def test_argument(self, arg1):
            return arg1

        def test_argument_type(self, arg1: int):
            return arg1

        def test_argument_opt(self, arg1='2'):
            return arg1

        def test_argument_opt_type(self, arg1: int=2):
            return arg1

        def test_argument_opt_multiple(self, arg1='2', barg='3'):
            return barg

        def test_argument_bool(self, arg1: bool):
            return arg1

        def test_argument_bool_false(self, arg1: bool=False):
            return arg1
