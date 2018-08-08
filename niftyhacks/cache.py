from __future__ import unicode_literals
import logging
import json
import os
import sys
import functools
import inspect
import csv
from io import BytesIO as StringIO

PYTHON2 = (sys.version_info.major == 2)
if PYTHON2:
    TEXT_TYPE = unicode # noqa
    BYTES_TYPE = str
else:
    TEXT_TYPE = str
    BYTES_TYPE = bytes # noqa

logger = logging.getLogger(__name__)

def to_kwargs(f, *args, **kwargs):
    """Takes arguments given to a function and converts all of them into
    keyword arguments by looking at the function signature.

    >>> def f(a, b=2): pass
    ...
    >>> to_kwargs(f, 1)
    {'a': 1, 'b': 2}
    >>> to_kwargs(f, 1, 3)
    {'a': 1, 'b': 3}
    >>> to_kwargs(f, b=3, a=1)
    {'a': 1, 'b': 3}
    """

    s = inspect.getargspec(f)
    defaults = s.defaults or []
    default_args = s.args[-len(defaults):]

    kw = {}
    kw.update(zip(default_args, defaults))
    kw.update(kwargs)
    kw.update(zip(s.args, args))
    return kw

def to_args(f, *args, **kwargs):
    """Takes arguments given to a function and converts all of them into
    positional arguments by looking at the function signature.

    >>> def f(a, b=2): pass
    ...
    >>> to_args(f, 1)
    [1, 2]
    >>> to_args(f, 1, 3)
    [1, 3]
    >>> to_args(f, b=3, a=1)
    [1, 3]
    """
    kwargs = to_kwargs(f, *args, **kwargs)
    s = inspect.getargspec(f)
    return [kwargs[a] for a in s.args]

class DiskCache(object):
    """Disk-based cache.

    Provides a memoize decorator.
    """
    def __init__(self, root):
        self.root = root

    def memoize(self, path):
        """Memoize decorator that uses disk as cache.

        If the path ends with .json, the return value is encoded into JSON
        before saving and decoded on read.
        
        String formatting opeator can be used in the path, the actual path
        is constructed by formatting the specified path using the argument
        values.
        
        Usage:

            cache = DiskCache("cache/")
        
            @cache.memoize("data/c_{number:02d}")
            def get_consititency(self, number):
                ...

            @cache.memoize("data/c_{1:02d}")
            def get_consititency(self, number):
                ...

        """
        path = os.path.join(self.root, path)
        def decorator(f):
            @functools.wraps(f)
            def g(*a, **kw):
                kwargs = to_kwargs(f, *a, **kw)
                args = to_args(f, *a, **kw)
                filepath = path.format(*args, **kwargs)            
                disk = Disk()
                content = disk.read(filepath)
                if content:
                    return content
                else:
                    content = f(*a, **kw)
                    content = disk.write(filepath, content)
                    return disk.read(filepath)
            return g
        return decorator

def safebytes(x):
    """Converts x to bytes type.

    bytes type is:
        - bytes in Python 3
        - str in Python 2

    Python 3:

        >>> safetext(1)
        b'1'
        >>> safetext(b'hello')
        b'hello'
        >>> safetext('hello')
        b'hello'

    Python 2:

        >>> safetext(1)
        '1'
        >>> safetext('hello')
        'hello'
        >>> safetext(u'hello')
        'hello'
    """
    if isinstance(x, (list, set)):
        return [safebytes(a) for a in x]
    elif isinstance(x, TEXT_TYPE):
        return x.encode('utf-8')
    elif isinstance(x, BYTES_TYPE):
        return x
    else:
        return safebytes(TEXT_TYPE(x))

def safetext(x):
    """Converts x to text type.

    text type is:
        - str in Python 3
        - unicode in Python 2

    Python 3:

        >>> safetext(1)
        '1'
        >>> safetext(b'hello')
        'hello'
        >>> safetext('hello')
        'hello'

    Python 2:

        >>> safetext(1)
        u'1'
        >>> safetext('hello')
        u'hello'
        >>> safetext(u'hello')
        u'hello'

    Also works with list of objects.

        >>> safe_text([1, b'hello', 'hello'])
        ['1', 'hello', 'hello']
    """
    if isinstance(x, (list, set)):
        return [safetext(a) for a in x]
    elif isinstance(x, BYTES_TYPE):
        return x.decode('utf-8')
    elif not isinstance(x, TEXT_TYPE):
        return TEXT_TYPE(x)
    else:
        return x


class Disk:
    """Simple wrapper to read and write files in various formats.

    This takes care of coverting the data to and from the required format. The default format is text.

    Other supported formats are:
        * json
    """
    def write(self, path, content):
        print("write({0!r}, {1!r})".format(path, content))
        if path.endswith(".json"):
            if inspect.isgenerator(content):
                content = list(content)
            content = json.dumps(content, indent=4)
        elif path.endswith(".csv"):
            f = StringIO()
            w = csv.writer(f)
            data = [safetext(row) for row in content]
            w.writerows(data)
            content = f.getvalue()
        elif path.endswith(".tsv"):
            f = StringIO()
            w = csv.writer(f, delimiter="\t")
            data = [safetext(row) for row in content]
            w.writerows(data)
            content = f.getvalue()

        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        logger.info("saving %s", path)
        with open(path, 'w') as f:
            f.write(content)

    def read(self, path):
        if os.path.exists(path):
            logger.info("reading %s", path)
            f = open(path)
            if path.endswith(".json"):
                return json.load(f)
            elif path.endswith(".csv"):
                reader = csv.reader(f)
                return list(reader)
            elif path.endswith(".tsv"):
                reader = csv.reader(f, delimiter="\t")
                return list(reader)
            else:
                return f.read()
            
def setup_logger():            
    FORMAT = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
