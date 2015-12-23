__author__ = 'sameer.pidadi'

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile


"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
TABLE_ROW = WORD_NAMESPACE + 'tr'
TABLE_COL = WORD_NAMESPACE + 'tc'

class DOCX_XMLExtractor:

    def __init__(self):
        pass

    def getText(self, path):
        """
        Take the path of a docx file as argument, return the text in unicode.
        """
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        tree = XML(xml_content)

        paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text
                     for node in paragraph.getiterator(TEXT)
                     if node.text]
            if texts:
                paragraphs.append(''.join(texts))

        paragraphs.append('TABLE_INFORMATION_ROW_WISE')

        for tablerow in tree.getiterator(TABLE_ROW):
            texts = [node.text
                     for node in tablerow.getiterator(TEXT)
                     if node.text]
            if texts:
                paragraphs.append(' '.join(texts))


        paragraphs.append('INFORMATION_EXTRACTED_FROM_HEADER')

        try:
            xml_content = document.read('word/header1.xml')
            document.close()
            tree = XML(xml_content)

            for paragraph in tree.getiterator(PARA):
                texts = [node.text
                         for node in paragraph.getiterator(TEXT)
                         if node.text]
                if texts:
                    paragraphs.append(''.join(texts))

        except Exception:
            document.close()
            pass






        return '\n\n'.join(paragraphs)