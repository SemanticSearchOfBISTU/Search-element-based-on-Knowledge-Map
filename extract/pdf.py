#coding=utf-8
import os

from PyPDF2 import PdfFileReader
from cffi.backend_ctypes import xrange
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def list_allfile(path,all_files=[]):
    if os.path.exists(path):
        files=os.listdir(path)#用于返回指定的文件夹包含的文件或文件夹的名字的列表
    else:
        print('this path not exist')
    for file in files:
        if os.path.isdir(os.path.join(path,file)):#判断某一路径是否为目录
            list_allfile(os.path.join(path,file),all_files)
        else:
            all_files.append(os.path.join(path,file))
    return all_files


if __name__ == "__main__":
    all_files=list_allfile(r'D:\isc_part')
    # file_handle = open('newtext.txt', mode='w')
    for path in all_files:
        pdf_title = PdfFileReader(path).getDocumentInfo().title  # 标题
        pdf_author = PdfFileReader(path).getDocumentInfo().author
        pdf_subject = PdfFileReader(path).getDocumentInfo().subject
        pdf_creator= PdfFileReader(path).getDocumentInfo().creator
        pdf_producer= PdfFileReader(path).getDocumentInfo().producer
        reader = PdfFileReader(path)
        page = reader.getNumPages()
        # data = open("C:/Users/rhy20/Desktop/newtext.txt", 'w+')
        print("***************************\n文件路径：",path,"\ntitle：",pdf_title,"\nauthors：",pdf_author,'\nabst：', pdf_subject,'\n创建者：',pdf_creator,'\n生产者：',pdf_producer,'\n页数：',page,"\n***************************\n")
        # data.close()
#         file_handle.write("***************************\n文件路径："+path+"\ntitle："+pdf_title+"\nauthors："+pdf_author+'\nabst：'+ pdf_subject+'\n创建者：'+pdf_creator+'\n生产者：'+pdf_producer+'\n页数：'+str(page)+"\n***************************\n")
# file_handle.close()

# 文件路径： D:\isc_part\10.5007\2175-7976.2008v15n20p205.pdf