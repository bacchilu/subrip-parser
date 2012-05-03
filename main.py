#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime


class Phrase(object):

    def __init__(
        self,
        index,
        startTime,
        endTime,
        content,
        ):

        self.index = index
        self.startTime = startTime
        self.endTime = endTime
        self.content = content

    def __add__(self, other):
        self.startTime += other
        self.endTime += other
        return self

    def __str__(self):
        return '''%d
%s --> %s
%s
''' % (self.index,
                self.startTime.strftime('%H:%M:%S,%f')[:-3],
                self.endTime.strftime('%H:%M:%S,%f')[:-3], self.content)


class SrtParser(object):

    def __init__(self, fp):
        self.fp = fp
        self.currentLine = None

    def nextLine(self):
        try:
            self.currentLine = self.fp.next().strip()
        except StopIteration:
            self.currentLine = None

    def parseNumber(self):
        try:
            return int(self.currentLine)
        except ValueError:
            raise Exception('Expecting a number')

    def parseTimes(self):
        assert len(self.currentLine) > 0
        try:
            return (datetime.datetime.strptime(self.currentLine[:12],
                    '%H:%M:%S,%f'),
                    datetime.datetime.strptime(self.currentLine[17:29],
                    '%H:%M:%S,%f'))
        except:
            raise Exception('Error in times parsing')

    def parseContent(self):
        assert len(self.currentLine) > 0
        ret = []
        try:
            while self.currentLine is not None \
                and len(self.currentLine) > 0:
                ret.append(self.currentLine)
                self.nextLine()
            return '\n'.join(ret)
        except:
            raise Exception('Error in parsing content')

    def parsePhrase(self):
        assert len(self.currentLine) > 0
        index = self.parseNumber()
        self.nextLine()
        (st, et) = self.parseTimes()
        self.nextLine()
        content = self.parseContent()
        assert self.currentLine is None or len(self.currentLine) == 0
        return Phrase(index, st, et, content)

    def skipBlankLines(self):
        while self.currentLine is not None and len(self.currentLine) \
            == 0:
            self.nextLine()

    def parse(self):
        ast = []
        self.nextLine()
        while True:
            if self.currentLine is None:
                return ast
            self.skipBlankLines()
            assert self.currentLine is None or len(self.currentLine) > 0
            if self.currentLine is None:
                return ast
            assert len(self.currentLine) > 0
            phrase = self.parsePhrase()
            ast.append(phrase)
            assert self.currentLine is None or len(self.currentLine) \
                == 0


if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        parser = SrtParser(fp)
        for e in parser.parse():
            print e + datetime.timedelta(seconds=15)
