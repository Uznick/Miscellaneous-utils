# -*- coding: utf-8 -*-

VERSION = (0, 1, 'alpha', 1)

from lxml import etree
import datetime

folder = 'evernote'

root = etree.Element('xml')
etree.SubElement(root, 'title').text = 'Evernote export'
etree.SubElement(root, 'link').text = 'http://evernote.com'
etree.SubElement(root, 'toodledoversion').text = '6'
etree.SubElement(root, 'description').text = 'Some data, exported from Evernote'

file = '%s' % ('etc/evernote.enex',)
result_file = '%s' % ('etc/result.xml',)

print "start parsing '%s' file" % file

parser = etree.XMLParser(strip_cdata=False)
evernote_xml = etree.parse(file, parser)
en_export = evernote_xml.xpath('/en-export')[0]

print 'application: %s' % en_export.attrib['application']
print 'export-date: %s' % en_export.attrib['export-date']
print 'version: %s' % en_export.attrib['version']

print 'generating xml'

for note in en_export.xpath('/en-export/note'):
    item = etree.Element('item')
    etree.SubElement(item, 'id')
    etree.SubElement(item, 'parent').text = '0'
    etree.SubElement(item, 'title').text = note.xpath('title')[0].text
    etree.SubElement(item, 'tag')
    etree.SubElement(item, 'folder').text = folder
    etree.SubElement(item, 'context')
    etree.SubElement(item, 'goal')
    etree.SubElement(item, 'location')

    created_date  = note.xpath('created')[0].text
    # how to work with these '20100414T203040Z' formatted dates, I wonder? Jut
    created_date = created_date.replace('T', '')
    created_date = created_date.replace('Z', '')
    created_date = datetime.datetime.strptime(created_date, '%Y%m%d%H%M%S')

    etree.SubElement(item, 'startdate').text = created_date.strftime('%Y-%m-%d')
    etree.SubElement(item, 'starttime').text = created_date.strftime('%H:%M')
    etree.SubElement(item, 'duedate')
    etree.SubElement(item, 'duedatemodifier')
    etree.SubElement(item, 'duetime')
    etree.SubElement(item, 'completed')
    etree.SubElement(item, 'repeat')
    etree.SubElement(item, 'priority').text = 'Low'
    etree.SubElement(item, 'length')
    etree.SubElement(item, 'timer').text = '0'
    etree.SubElement(item, 'status').text = 'None'
    etree.SubElement(item, 'star').text = '0'
    content = unicode(note.xpath('content')[0].text)

    # Content inside CDATA here is properly valid xhtml, so, we unescape it, remove entities and parse again
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&nbsp;', ' ')
    content = content.replace('<br/>', '\n')

    # ValueError: Unicode strings with encoding declaration are not supported, so we just
    content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')

    content = etree.fromstring(content)

    #print etree.tostring(content)

    content.tag = 'note'
    item.append(content)

    root.append(item)


#result = etree.tostring(root, encoding = 'utf-8', pretty_print =  True)
etree.ElementTree(root).write(result_file, encoding = 'utf-8')

print "file '%s' is saved" % result_file

print 'exit'