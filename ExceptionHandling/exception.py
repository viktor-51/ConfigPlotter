import errno
import os
import sys

def raise_exception_if_none_or_empty(value, message, err):
    if not value:
        errors[err](message)

def look_up_err(message):
    raise LookupError(message)

def file_not_found_err(message):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), message)

def do_print_if_exception(func, errors, messages, handling_func, args):
    try:
        return func(*args)
    except errors as err:
        index = errors.index(type(err))

        print("\n{}".format(messages[index]))
        handling_func()

def longer_then(left, right, err_msg):
    if len(left) < len(right):
        print(err_msg)
        sys.exit("exited by error")

def equal_to(left, right, err_msg):
    if not (left == right):
        print(err_msg)
        sys.exit("exited by error")

def want_to_quit():
    want_to_quit = int(input("do you want to quit?, 1 = yes, 0 = no\n : "))

    if want_to_quit:
        sys.exit("exited by user")


errors = {
    "LookupError" : look_up_err,
    "FileNotFoundError" : file_not_found_err
}
