import re

from .exceptions import FileSuffixError


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
        for line in self.file.readlines():
            indent = re.match('^[\s]+', line)
            print(indent, line, end='')

    def write(self):
        pass
