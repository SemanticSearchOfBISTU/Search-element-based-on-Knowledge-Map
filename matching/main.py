import math
import re
import heapq
import datetime
import time

import numpy as np
from elasticsearch import Elasticsearch
from nltk import word_tokenize
from nltk.corpus import stopwords


text1 = "Converging lines of evidence indicates "
text2 = "The aim of this study is to"


#链接es
es = Elasticsearch([{'host':'180.76.242.135','port':9200}], http_auth=('eswzj', '2019011415'), timeout=3600)
query_json = {
#指定需要显示的字段，类似表名
  "_source": [
      "abst"
      ],
  "query": {
    "bool": {
      "must": [
        [
          { "match_all": {} }
        ]
      ]
    }
  }
}
query_path = {
#指定需要显示的字段，类似表名
  "_source": [
      "path"
      ],
  "query": {
    "bool": {
      "must": [
        [
          { "match_all": {} }
        ]
      ]
    }
  }
}
query_title = {
#指定需要显示的字段，类似表名
  "_source": [
      "title"
      ],
  "query": {
    "bool": {
      "must": [
        [
          { "match_all": {} }
        ]
      ]
    }
  }
}
#查询结果
query = es.search(index='essay',body=query_json,scroll='15m',size=1000)
query1 = es.search(index='essay',body=query_path,scroll='15m',size=1000)
query2 = es.search(index='essay',body=query_title,scroll='15m',size=1000)

results = query['hits']['hits'] # es查询出的结果第一页
total = query['hits']['total']['value']  # es查询出的结果总量
scroll_id = query['_scroll_id'] # 游标用于输出es查询出的所有结果

results_path = query1['hits']['hits'] # es查询出的结果第一页
total_path = query1['hits']['total']['value']  # es查询出的结果总量
scroll_id_path = query1['_scroll_id'] # 游标用于输出es查询出的所有结果

results_title = query2['hits']['hits'] # es查询出的结果第一页
total_title = query2['hits']['total']['value']  # es查询出的结果总量
scroll_id_title = query2['_scroll_id'] # 游标用于输出es查询出的所有结果

abstdata=[]
pathdata=[]
titledata=[]

for i in range(0, int(total/100)+1):
    # scroll参数必须指定否则会报错
    query_scroll = es.scroll(scroll_id=scroll_id,scroll='15m')['hits']['hits']
    results += query_scroll
    for res in results:
        #获取只有表名和值
        abstdata.append(res["_source"])
        # print(res["_source"])

for i in range(0, int(total_title/100)+1):
    # scroll参数必须指定否则会报错
    query_scroll = es.scroll(scroll_id=scroll_id_title,scroll='15m')['hits']['hits']
    results_title += query_scroll
    for res in results_title:
        #获取只有表名和值
        titledata.append(res["_source"])
        # print(res["_source"])

for i in range(0, int(total_path/100)+1):
    # scroll参数必须指定否则会报错
    query_scroll = es.scroll(scroll_id=scroll_id_path,scroll='15m')['hits']['hits']
    results_path += query_scroll
    for res in results_path:
        #获取只有表名和值
        pathdata.append(res["_source"])
        #print(res["_source"])
# abstdata = " ".join('%s' %id for id in abstdata)
# list(eval(abstdata))
# print(abstdata)
# a = str(abstdata[0])
number = len(abstdata)
number = number-1
num_path = len(pathdata)
num_path-=1
# print(num_path)
# print(type(a[0]))
# print(a)

def compute_cosine(text_a, text_b):
    english_stopwords = set(stopwords.words('english'))
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', ' ']

    word_tokens1 = word_tokenize(text_a)
    words_stop1 = [word for word in word_tokens1 if not word in english_stopwords]
    texts_filtered1 = [word for word in words_stop1 if not word in english_punctuations]

    words_mid1 = np.array(texts_filtered1)
    str1 = ",".join(words_mid1)  # 转换为str类型
    # print(str1);

    word_tokens2 = word_tokenize(text_b)
    words_stop2 = [word for word in word_tokens2 if not word in english_stopwords]
    texts_filtered2 = [word for word in words_stop2 if not word in english_punctuations]
    words_mid2 = np.array(texts_filtered2)  # 转换类型
    str2 = ",".join(words_mid2)
    #rint(words1)

    words1 = str1.split(",");  # 使用默认分隔符,分词，只能处理str类型
    words2 = str2.split(",");
    words1_dict = {}
    words2_dict = {}
    for word in words1:
        if word != '' and word in words1_dict:
            num = words1_dict[word]
            words1_dict[word] = num + 1
        elif word != '':
            words1_dict[word] = 1
        else:
            continue

    for word in words2:
        if word != '' and word in words2_dict:
            num = words2_dict[word]
            words2_dict[word] = num + 1
        elif word != '':
            words2_dict[word] = 1
        else:
            continue
    dic1 = sorted(words1_dict.items(), key=lambda asd: asd[1], reverse=True)
    dic2 = sorted(words2_dict.items(), key=lambda asd: asd[1], reverse=True)

    # 得到词向量
    words_key = []
    for i in range(len(dic1)):
        words_key.append(dic1[i][0])  # 向数组中添加元素
    for i in range(len(dic2)):
        if dic2[i][0] in words_key:
            # print 'has_key', dic2[i][0]
            pass
        else:  # 合并
            words_key.append(dic2[i][0])
    # print(words_key)
    vect1 = []
    vect2 = []
    for word in words_key:
        if word in words1_dict:
            vect1.append(words1_dict[word])
        else:
            vect1.append(0)
        if word in words2_dict:
            vect2.append(words2_dict[word])
        else:
            vect2.append(0)


    # 计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(vect1)):
        sum += vect1[i] * vect2[i]
        sq1 += pow(vect1[i], 2)
        sq2 += pow(vect2[i], 2)
    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        result = 0.0
    # result = str(result)
    #print(result)
    return result

def match_es_word(text):
    list_totle=[]
    begin_time = datetime.datetime.now()
    begin = time.time()
    max = 0.0
    path_num = 0
    max_match = 'ast'
    # 匹配度
    match_sort=[]
    for i in range(number):
        a = str(abstdata[i])
        mid = compute_cosine(text, a)
        if mid > 0.1:
            match_sort.append(mid)
        if mid>max:
            max = mid
            max_match = a
            path_num = i
    print(max)
    print(titledata[path_num])
    print(pathdata[path_num])
    print(max_match)
    # re1 = heapq.nlargest(10, match_sort)    # 求最大的10个元素，并排序
    # match_index = map(match_sort.index, heapq.nlargest(10, match_sort))  # 求最大的10个索引
    # print(re1)
    # print(match_index)
    list_totle.append(max)
    list_totle.append(titledata[path_num])
    list_totle.append(pathdata[path_num])
    list_totle.append(max_match)  #摘要
    end_time = datetime.datetime.now()
    end = time.time()
    print("datatime:", end_time - begin_time)
    print("time:", end - begin)
    return list_totle



if __name__ == '__main__':
     match_es_word(text1)
#     begin_time = datetime.datetime.now()
#     begin = time.time()
#     max = 0.0
#     path_num = 0
#     max_match = 'ast'
#     i = 0
# for i in range(number):
#     a = str(abstdata[i])
#     mid = compute_cosine(text2, a)
#     if mid>max:
#         max = mid
#         max_match = a
#         path_num = i
#
# print(max)
# print(titledata[path_num])
# print(pathdata[path_num])
# print(max_match)
#
# end_time = datetime.datetime.now()
# end = time.time()
# print("datatime:", end_time - begin_time)
# print("time:", end - begin)
