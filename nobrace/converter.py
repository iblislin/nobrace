import re

from collections import Counter

from .exceptions import FileSuffixError
from .stack import IndentStack


class Converter:

    def __init__(self, filename, output_name=None):
        self._output_name = output_name
        self.file = open(filename, 'r')

    def __del__(self):
        self.file.close()

    def check_filename(self, filename):
        '''
        Check filename suffix, it should be end with 'x'.
        e.g. test.cppx
        '''
        if self.filename[-1] != 'x':
            raise FileSuffixError()

    @property
    def output_name(self):
        self.check_filename(filename)

        if self._output_name:
            return self._output_name

        return self._output_name[:-1]

    @output_name.setter
    def output_name(self, name):
        self._output_name = name

    @property
    def output_file(self):
        if not self._output_file:
            return open(self.output_file, 'w')
        return open(self._output_file)

    def convert(self):
        indent_stack = IndentStack([''])
        blankline_stack = Counter()


        def push_blankline(indent):
            blankline_stack[indent] = blankline_stack.get(indent, 0) + 1

        def pop_blankline(indent):
            if blankline_stack.get(indent) is None:
                return
            print('\n' * blankline_stack.pop(indent), end='')

        def complete_brace(indent, cur_indent):
            if indent == cur_indent:
                pop_blankline(indent)
                return

            if len(indent) > len(cur_indent):
                print(indent_stack.push(indent))
            elif len(indent) < len(cur_indent):
                print(indent_stack.pop())
            else:
                pop_blankline(cur_indent)

            try:
                complete_brace(indent, indent_stack.top)
            except IndexError:
                return

        def semicolon_complete(line: str) -> str:
            _l = line.rstrip()
            if _l[-1] == ':':
                return _l[:-1] + '\n'
            return _l + ';\n'

        for line in self.file.readlines():
            indent_match = re.match('^([ \t]+)[\S]+', line)
            cur_indent = indent_stack[-1]

            if indent_match:
                indent = indent_match.group(1)
            else:
                indent = None
                if cur_indent:
                    push_blankline(cur_indent)
                else:
                    print(line, end='')
                continue

            _line = semicolon_complete(line)
            complete_brace(indent, cur_indent)
            print(_line, end='', sep=', ')

        # handle eol
        print('{}}}'.format(indent_stack[-2]))


    def write(self):
        pass
