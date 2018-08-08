"""
    texar: text archive
    ~~~~~~~~~~~~~~~~~~~

texar is a simple text-based archive format. Think of like a more texual version of tar.

Here is a sample archive:

    == numbers.txt
    1
    2
    3
    == sum.txt
    6

The above archive contains 2 files, namely ``numbers.txt`` and ``sum.txt``.

As you can guess, each file starts with a separator line. The separator line starts with ``==``
prefix followed by the filename. It is assumed that the prefix will not appear at the beginning
of any line in any of the files in the archive.

If required, a custom prefix can be selected by specifying the separator in
the optional headers section. (this feature is not yet implemented)

    separator: ====>
    ====> numbers.txt
    1
    2
    3
    ====> sum.txt
    6

This is very handy when you need to work with multiple files, but want to
write all off them at a single place.

Testing programs that take files as inputs and produce other files is very
good use case. For example:

    == command
    head -3
    == input
    1
    2
    3
    4
    5
    == output
    1
    2
    3
"""
import re

def parse(archive_contents):
    """Parses the archive contents returns the file contents as a dictionary.
    """
    re_marker = re.compile("^( *)== *(.*)$")
    def parse():
        lines = []
        filename = None
        indent = ""

        for line in archive_contents.splitlines():
            m = re_marker.match(line)
            if m:
                yield filename, "".join(lines)
                lines = []
                indent, filename = m.groups()
                filename = filename.strip()
            else:
                line = line[len(indent):] + "\n"
                lines.append(line)

        yield filename, "".join(lines)

    d = dict(parse())
    d.pop(None, None) # Remove the empty entry
    return d
