# -*- coding=utf-8 -*-
import numpy as np
import pandas as pa
import csv

'''加载词库'''


def load_embedding(embedding_path):
    embedding_list = list()
    count = 0
    for line in open(embedding_path, encoding='utf-8'):
        line = line.strip()
        embedding_list.append(line)
        count += 1
        if count % 1000 == 0:
            print(count, 'loaded')
    print('loaded %s word embedding, finished' % count, )
    res = np.array(embedding_list)
    return res
    # return embedding_list

    '''生成元素'''


def process0(myDict):
    print('==========process0==========')
    out = open('test6.csv', 'a', encoding='utf-8', newline='')
    csv_write = csv.writer(out, dialect='excel')
    raw_list = []
    raw_list.append('_id')
    raw_list.append('实体')
    csv_write.writerow(raw_list)
    for i, mystr in enumerate(myDict):
        raw_list = []
        raw_list.append(i)
        # print(mystr)
        raw_list.append(mystr)
        csv_write.writerow(raw_list)
        if i % 10000 == 0:
            print('写入的实体数量：', i)
    out.close()


'''生成三元组'''


def process1(myDict):
    print('====================')
    raw_data = []
    for i, mystr in enumerate(myDict):
        # for i,mystr in range(0,len(a)):
        j = i + 1
        if (j < len(myDict) - 1):
            nextStr = myDict[j]
            while (j < len(myDict) - 1):
                if (mystr in nextStr):
                    raw_list = []
                    raw_list.append(nextStr)
                    raw_list.append('subclass of')
                    raw_list.append(mystr)
                    raw_data.append(raw_list)
                j = j + 1
                nextStr = myDict[j]
    name = ['实体', '关系', '实体']
    test = pa.DataFrame(columns=name, data=raw_data)
    test.to_csv('res.csv', encoding='utf-8')

    '''生成三元组'''

def process2(myDict):
    print('==========process2==========')
    out = open('test4.csv', 'a', encoding='utf-8', newline='')
    csv_write = csv.writer(out, dialect='excel')
    raw_list = []
    raw_list.append('_from')
    raw_list.append('关系')
    raw_list.append('_to')
    csv_write.writerow(raw_list)
    count = 0
    for i, mystr in enumerate(myDict):
        j = i + 1
        if (j < len(myDict) - 1):
            nextStr = myDict[j]
            while (j < len(myDict) - 1):
                if (mystr in nextStr):
                    raw_list = []
                    str1 = 'test4/' + str(j);
                    str2 = 'test4/' + str(i);
                    raw_list.append(str1)
                    raw_list.append('subclass of')
                    raw_list.append(str2)
                    csv_write.writerow(raw_list)
                    count = count + 1
                j = j + 1
                nextStr = myDict[j]
        if i % 1000 == 0:
            print('匹配到位置：', i)
        if (count % 10000 == 0):
            print('已写入三元组的数量： ', count)
    out.close()

    '''生成三元组3'''


def process3(myDict):
    print('==========process2==========')
    out = open('test6_edge.csv', 'a', encoding='utf-8', newline='')
    csv_write = csv.writer(out, dialect='excel')
    raw_list = []
    raw_list.append('_from')
    raw_list.append('关系')
    raw_list.append('_to')
    csv_write.writerow(raw_list)
    count = 0
    for i, mystr in enumerate(myDict):
        j = i + 1
        if (j < len(myDict) - 1):
            nextStr = str(myDict[j])
            while (j < len(myDict) - 1):
                mystr2 = str(mystr)
                num = nextStr.find(mystr2)
                if num != -1:
                    if num == len(nextStr) - len(mystr):
                        raw_list = []
                        str1 = 'test6/' + str(j);
                        str2 = 'test6/' + str(i);
                        raw_list.append(str1)
                        raw_list.append('subclass of')
                        raw_list.append(str2)
                        csv_write.writerow(raw_list)
                        count = count + 1
                    else:
                        raw_list = []
                        str1 = 'test6/' + str(j);
                        str2 = 'test6/' + str(i);
                        raw_list.append(str1)
                        raw_list.append('is related to')
                        raw_list.append(str2)
                        csv_write.writerow(raw_list)
                        count = count + 1
                j = j + 1
                nextStr = str(myDict[j])
        if (i % 10000 == 0):
            print('匹配到位置：', i)
        if (count % 10000 == 0):
            print('已写入三元组的数量： ', count)
    out.close()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 加载词库
    embedding_path = ("litleMergeWord.txt")
    # embedding_path = ("mergeWord.txt")
    d = load_embedding(embedding_path)
    print('------------------------------1/加载完成----------------------------------------')

    process0(d)
    print('------------------------------2/实体(test6.csv)生成完成------------------------------------')

    process3(d)
    print('-----------------------------3/三元组(test6_edge)生成结束------------------------------------')

