#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Mathias Payer <mathias@nebelwelt.net>"
__description__ = "Script to generate the publication html structure based on the XML."

import xml.etree.ElementTree as ET
import sys
from argparse import ArgumentParser

venues = {}
def parseVenues(xmldoc):
    for e in xmldoc.findall('venues/*'):
        venues[e.attrib['short']] = e.text

def handleBibs(xmldoc, venue):
    name = 'inproceedings'
    #if venue == 'report':
    #    name = 'misc'
    if venue == 'thesis':
        name = 'thesis'
    if venue == 'magazine':
        name = 'article'
    counter = 0
    ret = ''
    for e in xmldoc.findall('publications/publication/[@type="'+venue+'"]'):
        counter = counter + 1
        ret += '@' + name + '{'
        filename = ''
        if e.find('filename') != None:
            filename = e.attrib['year'][2:] + e.find('filename').text
        else:
            filename = e.attrib['year'][2:] + e.find('shortvenue').text
        first = ''
        authors = ''
        for author in e.find('authors'):
            if first == '':
                # TODO must be last index
                first = author.text.strip().lower() #[author.text.index(' ')+1:].lower()
                while first.find(' ') != -1:
                    first = first[first.index(' ')+1:]
                while first.find('\'') != -1:
                    first = first[first.index('\'')+1:]
            authors += author.text + ' and '
        authors = authors[:-5]
        key = ''
        if venue != 'thesis':
            if 'key' in e.attrib:
                key = e.attrib['key']
            else:
                key = e.find('shortvenue').text.lower()
            ret += first + e.attrib['year'][2:] + key + ',\n'
        else:
            ret += first + e.attrib['year'][2:] + ',\n'
        ret += '  author = {' + authors + '},\n'
        ret += '  title = {{' + e.find('title').text + '}},\n'
        ret += '  year = {' + e.attrib['year'] + '},\n'
        if name == 'inproceedings' and venue != 'report':
            #ret += '  booktitle = ' + e.find('shortvenue').text + ',\n'
            ret += '  booktitle = {' + venues[e.find('shortvenue').text] + '},\n'
        if name == 'article':
            #ret += '  journal = ' + e.find('shortvenue').text + ',\n'
            ret += '  journal = {' + venues[e.find('shortvenue').text] + '},\n'
        if venue == 'report':
            if 'report' in e.attrib:
                ret += '  booktitle = {' + venues[e.find('shortvenue').text] + '},\n'
                #ret += '  booktitle = ' + e.find('shortvenue').text + ',\n'
            else:
                ret += '  booktitle = {' + venues[e.find('shortvenue').text]
                ret += ' \\url{http://nebelwelt.net/publications/files/' + filename + '.pdf}},\n'
        if e.find('doi') != None:
            ret += '  doi = {' + e.find('doi').text + '},\n'
        if e.find('stats') != None:
            stats = e.find('stats')
            details = ''
            if 'accept' in stats.attrib:
                rate = str(float(stats.attrib['accept'])/float(stats.attrib['submissions'])*100)
                rate = rate[0:rate.find('.')]
                details = '{}\\% acceptance rate -- {}/{}'.format(rate, stats.attrib['accept'], stats.attrib['submissions'])
            note = ''
            if e.find('note') != None:
                note = '\\textbf{' + e.find('note').text + '}'
            if note != '' and details !='':
                note = note + ' ,'
            ret += '  pages = {(' + note + details + ')},\n'
        ret += '  keywords = {' + venue + '},\n'
        if venue == 'thesis':
            if counter == 1:
                ret += '  type = {PhD Thesis},\n'
            if counter == 2:
                ret += '  type = {Master Thesis},\n'
            if counter > 2:
                ret += '  type = {Bachelor Project Thesis},\n'
        ret += '}\n\n'
    return ret

def handlePublications(xmldoc, venue, title):
    ret =  '<h4>' + title + '</h4>\n'
    prevyear = '0'
    for e in xmldoc.findall('publications/publication/[@type="'+venue+'"]'):
        # Print title
        ret += '<p class="publication">\n'
        if e.find('filename') != None:
            filename = e.attrib['year'][2:] + e.find('filename').text
        else:
            filename = e.attrib['year'][2:] + e.find('shortvenue').text
        if e.find('note') != None:
            note = '<b>' + e.find('note').text + '</b>'
        else:
            note = ''
        if not 'report' in e.attrib:
            ret += '<b><a href="./files/' + filename + '.pdf" name="'+filename+'">' + e.find('title').text + '</a></b>'
        else:
            ret += '<b><u><a name="'+filename+'">' + e.find('title').text + '</a></u></b>'
        if prevyear != e.attrib['year']:
            prevyear = e.attrib['year']
            ret += '<span class="float-right"><b>'+prevyear+'</b></span><br/>'
        else:
            ret += '<br/>'
        # Print authors
        for author in e.find('authors')[:-1]:
            ret += author.text + ', '
        if len(e.find('authors')) > 1:
            ret += 'and '
        ret += e.find('authors')[-1].text + '.<br/>'
        # Print Venue
        if e.find('shortvenue') != None:
            ret += 'In <i><b>' + e.find('shortvenue').text + "'" + e.attrib['year'][2:] + '</b>: '
            ret += venues[e.find('shortvenue').text] + ', ' + e.attrib['year'] + '</i>'
            if e.find('shortvenue').text not in venues:
                print("OOps, {} is not in venues.".format(e.find('shortvenue').text))
        else:
            ret += 'In <i>' + e.find('venue').text + '</i>'
        # Do we have any additional remarks (links, notes, presentation)?
        addon = ''
        if 'presentation' in e.attrib:
            addon = '<a href="./files/' + filename + '-presentation.pdf">presentation</a>, '
        if note != '':
            addon = addon + ' ' + note + ', '
            addon = addon.lstrip()
        if e.find('links') != None:
            for link in e.find('links'):
                addon = addon + '<a href="' + link.attrib['href'] + '">' + link.attrib['name'] + '</a>, '
        if e.find('doi') != None:
            addon = addon + '<a href="http://dx.doi.org/' + e.find('doi').text + '">DOI</a>, '
        if addon != '':
            addon = addon[0:-2]
            ret += ' (' + addon + ')'
        ret += '</p>'
    return ret

if __name__ == "__main__":
    parser = ArgumentParser(description=__description__)
    parser.add_argument('-t', '--template', type=str, metavar='template filename', help='Filename for the template to use.', required=False)
    parser.add_argument('-o', '--out', type=str, metavar='output filename', help='Filename to write output', required=True)
    parser.add_argument('-p', '--publications', type=str, metavar='publications file', help='XML file containing publications', required=False, default='publications.xml')
    parser.add_argument('-T', '--type', type=str, metavar='type', help='Output type. Values: {html | bib}', required=False, default='html')
    args = parser.parse_args()

    pubs = ET.parse(args.publications)
    parseVenues(pubs)

    ret = ''
    if args.type == 'html':
        txt = open(args.template).read()
        ret += txt[0:txt.find('###CONTENT###')]
        ret += handlePublications(pubs, 'conference', 'Conference Proceedings')
        ret += handlePublications(pubs, 'journal', 'Journal and Magazine Publications')
        ret += handlePublications(pubs, 'workshop', 'Workshop Proceedings')
        ret += handlePublications(pubs, 'collection', 'Books and Chapters')
        ret += handlePublications(pubs, 'report', 'Technical Reports and Hacker Conferences')
        if args.template == "nebelwelt.html":
            ret += handlePublications(pubs, 'thesis', 'Theses')
        # TODO: student theses
        ret += txt[txt.find('###CONTENT###')+13:]
    if args.type == 'bib':
        #for i in venues:
        #    ret +='@string{' + i + '="' + venues[i] + '"}\n'
        #ret += '\n\n'
        ret += handleBibs(pubs, 'collection')
        ret += handleBibs(pubs, 'journal')
        ret += handleBibs(pubs, 'conference')
        ret += handleBibs(pubs, 'workshop')
        ret += handleBibs(pubs, 'report')
        ret += handleBibs(pubs, 'thesis')
        
    with open(args.out, 'w') as f:
        f.write(ret)
        f.close()
