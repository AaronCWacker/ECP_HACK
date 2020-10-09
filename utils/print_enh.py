import inspect


def _prefix(label: str=''):
    calling_frame = inspect.currentframe().f_back.f_back
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(calling_frame)
    return f'{filename} {line_number}: {function_name}(...) {label}> \t '


def print_begin(*args, sep=' ', end='\n', file=None, ret_value='') -> str:
    """Print the function name and start."""
    print(_prefix('begin'), *args, sep=sep, end=end, file=file, flush=True)
    return ret_value


def print_end(*args, sep=' ', end='\n', file=None, ret_value='') -> str:
    """Print the function name and stop."""
    print(_prefix('end'), *args, sep=sep, end=end, file=file, flush=True)
    return ret_value


def print_plus(*args, sep=' ', end='\n', file=None) -> str:
    """Print the function name."""
    print(_prefix(), *args, sep=sep, end=end, file=file, flush=True)
    return f'{_prefix()} {args}'


if __name__ == '__main__':
    val = print_plus('sample', 'other', 'also')
    print(val)
    val = print_plus({'sample': 2, 'other': 'hello'})
    print(val)
