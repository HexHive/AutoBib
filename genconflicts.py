#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Mathias Payer <mathias@nebelwelt.net>"
__description__ = "Script to generate the recent list of conflicts based on the XML."

import xml.etree.ElementTree as ET
import sys
from argparse import ArgumentParser
import datetime

def getConflicts(xmldoc, from_year):
    coauthors = set()
    for e in xmldoc.findall('publications/publication'):
        if int(e.attrib['year']) >= from_year:
            for author in e.find('authors'):
                coauthors.add(author.text)
    return coauthors


if __name__ == "__main__":
    parser = ArgumentParser(description=__description__)
    parser.add_argument('-p', '--publications', type=str, metavar='publications file', help='XML file containing publications', required=False, default='publications.xml')
    parser.add_argument('-a', '--adviser', type=str, metavar='adviser file', help='Text file with adviser relationship', required=False, default='adviser.txt')
    parser.add_argument('-y', '--years', type=int, metavar='year count', help='Get conflicts for N years, default: 2', required=False, default=2)
    args = parser.parse_args()

    pubs = ET.parse(args.publications)

    from_year = datetime.date.today().year - args.years

    conflicts = getConflicts(pubs, from_year)

    for author in open(args.adviser, 'r').readlines():
        conflicts.add(author.strip())

    for author in sorted(conflicts):
        print(author)