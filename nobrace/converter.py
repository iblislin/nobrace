import abc
import re

from .exceptions import FileSuffixError
from .stack import LineCounter, IndentStack


class ConverterBase(metaclass=abc.ABCMeta):

    def __init__(self, src: str):
        self.src = src
        self.code_blocks

    @property
    def code_blocks(self):
        '''
        Aggregate code block into tuple.
        A code block could be determined by intentation.
        '''
        indent_stack = IndentStack([''])
        blankline_stack = LineCounter()

        def complete_brace(indent, cur_indent):
            if indent == cur_indent:
                print('\n' * blankline_stack.pop(cur_indent, 0))
                return

            if len(indent) > len(cur_indent):
                print(indent_stack.push(indent))
            elif len(indent) < len(cur_indent):
                print(indent_stack.pop())
            else:
                print('\n' * blankline_stack.pop(cur_indent, 0))

            try:
                complete_brace(indent, indent_stack.top)
            except IndexError:
                return

        for line in self.src.split('\n'):
            indent_match = re.match('^([ \t]+)[\S]+', line)
            cur_indent = indent_stack[-1]

            if indent_match:
                indent = indent_match.group(1)

                complete_brace(indent, cur_indent)
                print(line, sep=', ')
            else:
                indent = None
                if cur_indent:
                    blankline_stack.push(cur_indent)
                else:
                    print(line)
        del line

        # handle eol
        print('{}}}'.format(indent_stack[-2]))
