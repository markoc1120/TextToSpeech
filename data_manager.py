import PyPDF2
import re
import os
from pathlib import Path


class DataManager:
    content = '<speak>'
    paths = list()
    searched_paths = list()

    def __init__(self):
        self.get_files_path()

    def read_pdf(self, filename):
        pdf_file_obj = open(filename, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

        for i in range(pdf_reader.numPages):
            page_obj = pdf_reader.getPage(i)

            if self.content is not None:
                self.content += page_obj.extractText()
            else:
                self.content = page_obj.extractText()

        self.content += '</speak>'

        pdf_file_obj.close()
        return self.content

    def clean_text(self):
        clean_text = re.sub('(\n)[a-zA-Z0-9]', 'New line <amazon:breath duration="medium"/>\n', self.content)
        return clean_text

    def get_files_path(self):
        home = str(Path.home())
        dir_path = os.path.dirname(os.path.realpath(home))

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.pdf'):
                    file_path = root+'/'+str(file)

                    if 'Relocated' not in file_path:
                        self.paths.append(file_path)

    def search_file_path(self, fn):
        for el in self.paths:
            if fn in el:
                self.searched_paths.append(el)
        return self.searched_paths
