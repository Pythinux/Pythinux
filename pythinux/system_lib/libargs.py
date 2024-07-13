import argparse

class ArgumentParser(argparse.ArgumentParser):
    """
    This is a wrapper around argparse.ArgumentParser that is designed for Pythinux. 
    It enforces some requirements, like passing `prog` to the constructor and `args` to `parse_args()`.
    It also automates and handles error reporting and makes using `argparse` as easy as doing it natively.
    """
    def __init__(self, prog, **kwargs):
        assertTrue(isinstance(prog, str))
        super().__init__(prog, **kwargs)
        self.exit_on_error = False
    def parse_args(self, args):
        assertTrue(isinstance(args, list))
        try:
            return super().parse_args(args)
        except argparse.ArgumentError as e:
            print("{}: error: {}".format(self.prog, e))
            raise SystemExit(e)
