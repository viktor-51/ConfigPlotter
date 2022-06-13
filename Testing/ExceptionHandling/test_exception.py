import unittest

from ExceptionHandling import exception 

class Test_Axis_Store(unittest.TestCase):
    def test_do_print_if_exception(self):
        def do_error():
            raise FileNotFoundError 

        func = do_error
        errors = (FileNotFoundError, )
        messages = ["did not find file"]
        handling_func = lambda : None

        exception.do_print_if_exception(func, errors, messages, handling_func)
    
    def test_do_print_if_exception_multiple(self):
        def do_error():
            raise FileExistsError 

        func = do_error
        errors = (FileNotFoundError, FileExistsError)
        messages = ["did not find file", "file exist error"]
        handling_func = lambda : None

        exception.do_print_if_exception(func, errors, messages, handling_func)
    
    def test_do_print_if_exception_multiple_args(self):
        def do_error(a, b):
            raise ValueError 

        def help_func():
            print("runing help")

        func = do_error
        errors = (FileNotFoundError, ValueError, FileExistsError)
        messages = ["did not find file", "file exist error"]
        handling_func = help_func

        exception.do_print_if_exception(func, errors, messages, handling_func, 50, 20)
    
#def do_print_if_exception(func, error, message, handling_func, *args):

 
