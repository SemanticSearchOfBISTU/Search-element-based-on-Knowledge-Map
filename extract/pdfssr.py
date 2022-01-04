import os
import re

import pdfplumber
import pandas as pd

# with pdfplumber.open("D:\isc_part/10.3389/fpsyt.2020.580863.pdf") as pdf:
#         print(pdf.metadata)

from PyPDF2 import PdfFileReader, PdfFileWriter
from cffi.backend_ctypes import xrange
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def list_allfile(path,all_files=[]):
    if os.path.exists(path):
        files=os.listdir(path)
    else:
        print('this path not exist')
    for file in files:
        if os.path.isdir(os.path.join(path,file)):
            list_allfile(os.path.join(path,file),all_files)
        else:
            all_files.append(os.path.join(path,file))
    return all_files


if __name__ == "__main__":
    all_files=list_allfile(r'D:\isc_part')
    for path in all_files:
            with pdfplumber.open(path) as pdf:
                print( "***************************\n路径：", path)
                print(pdf.metadata)
                print("总页数：",len(pdf.pages))


                # from PyPDF2 import PdfFileReader, PdfFileWriter
                # import pdfplumber
                #
                # path = r'D:\isc_part\10.3389/fpsyt.2020.584501.pdf'
                # pdf_writer = PdfFileWriter()
                # pdf_reader = PdfFileReader(path)
                # with pdfplumber.open(path) as pdf:
                #     for i in range(pdf_reader.getNumPages()):
                #         page = pdf.pages[i]
                #         if 'RESULTS' in page.extract_text():
                #             pattern=re.compile('RESULTS.+.')
                #             str = page.extract_text()
                #             print(str)
                #             result = pattern.findall(str)
                #             print(result)
                #             # print(i + 1, page.extract_text())



