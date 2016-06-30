#!/usr/bin/env python


import PyPDF2
import sys


def clean():
    input_file_name = sys.argv[1]
    out_file_name = sys.argv[1]
    if len(sys.argv) >= 3:
        out_file_name = sys.argv[2]

    pdf_reader = PyPDF2.PdfFileReader(input_file_name)
    pdf_writer = PyPDF2.PdfFileWriter()

    link = 'http://www.it-ebooks.info/'

    num_pages = pdf_reader.getNumPages()
    for i in range(0, num_pages):
        print 'scanning page: ', i

        page = pdf_reader.getPage(i)
        for indirect_annot in page['/Annots']:
            obj = pdf_reader.getObject(indirect_annot)
            if obj.has_key('/A') and obj['/A'].has_key('/URI'):
                uri = obj['/A']['/URI']
                if str(uri) == link:
                    print 'removing link ', str(uri)
                    page['/Annots'].remove(indirect_annot)

        for indirect_content in page['/Contents']:
            content_obj = pdf_reader.getObject(indirect_content)
            if content_obj.getData().find('(www.it-ebooks.info)') >= 0:
                print 'removing text (www.it-ebooks.info)'
                page['/Contents'].remove(indirect_content)

        pdf_writer.addPage(page)

    out_file = open(out_file_name, 'wb')
    pdf_writer.write(out_file)
    out_file.close()

if len(sys.argv) < 2:
    print 'Usage: ThankYouEBooks.py input.pdf output.pdf'
else:
    clean()
