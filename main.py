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
        self.nextLine()
        try:
            return (datetime.datetime.strptime(self.currentLine[:12],
                    '%H:%M:%S,%f'),
                    datetime.datetime.strptime(self.currentLine[17:29],
                    '%H:%M:%S,%f'))
        except:
            raise Exception('Error in times parsing')

    def parseContent(self):
        ret = []
        self.nextLine()
        try:
            assert self.currentLine != ''
            while self.currentLine != '' and self.currentLine \
                is not None:
                ret.append(self.currentLine)
                self.nextLine()
            return '\n'.join(ret)
        except:
            raise Exception('Error in parsing content')

    def parsePhrase(self):
        index = self.parseNumber()
        (st, et) = self.parseTimes()
        content = self.parseContent()
        return Phrase(index, st, et, content)

    def parse(self):
        ast = []
        while True:
            self.nextLine()
            if self.currentLine is not None:
                phrase = self.parsePhrase()
                ast.append(phrase)
            else:
                return ast


if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        ast = SrtParser(fp).parse()
        for p in ast:
            print p + datetime.timedelta(seconds=15)
