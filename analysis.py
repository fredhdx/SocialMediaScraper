# -*- coding: utf-8 -*-
"""
来自：Github(dingmyu/weibo_analysis)
"""

# import pandas as pd
import re
import jieba
import jieba.analyse
from collections import Counter
import jieba.posseg as pseg
import keywords_new
import os


def analyze(user_id):
    basepath = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(user_id)
    filepath = basepath+ os.path.sep + str(user_id) + "-compact.txt"

    if not os.path.isfile(filepath):
        print(filepath + "不存在")
        return None

    f = open(filepath,"r")
    f1 = open(basepath + os.path.sep + "category.txt", "w")
    f2 = open(basepath + os.path.sep + "express.txt", "w")
    f3 = open(basepath + os.path.sep + "word.txt", "w")
    f4 = open(basepath + os.path.sep + "name.txt", "w")
    list1 = []
    record = {}  # 记录命中信息
    express = {}
    name_set = {}

    for line in f:
        line = line.strip()
        if line:
            item = line.split(' ', 1)[1]
            ex_all = re.findall(u"\\[.*?\\]", item)
            if ex_all:
                for ex_item in ex_all:
                    express[ex_item] = express.get(ex_item, 0) + 1
            for kw, keywords in keywords_new.keyword_dict.items():  # kw是大类
                flag = 0  # 大类命中的标志
                for key, keyword in keywords.items():  # key 是小类
                    if flag == 1:
                            break
                    for word in keyword:  # 小类关键词
                        match_flag = 1  # 列表中关键词全部命中的标志
                        for small_word in word:  # 关键词列表
    #                    	print(small_word)
                            match = re.search(re.compile(small_word, re.I), item)
                            if not match:
                                match_flag = 0
                                break
                        if match_flag == 1:  #命中了一个小类
                            record[kw] = record.get(kw, 0) + 1 # 单次记录
                            flag = 1
                            break
            item = re.sub(u"\\[.*?\\]", '', item)
            list = jieba.cut(item, cut_all = False)
            for ll in list:
                list1.append(ll)  # 分词
            seg_list = pseg.cut(item)
            for word, flag in seg_list:
                if flag == 'nr':
                    name_set[word] = name_set.get(word, 0) + 1


    print("完成建造")
    print("express dict size: " + str(len(express)))
    for key,keywords in express.items():
        print(key + ': ' + str(express[key]))

    count = Counter(list1)
    for item in sorted(dict(count).items(), key=lambda d:d[1], reverse = True):
        if len(item[0]) >= 2 and item[1] >= 3:
            f3.write(str(item[0]) + ' ' + str(item[1]) + '\n')

    for key, keywords in sorted(record.items(), key=lambda d:d[1], reverse = True):
        f1.write(u'命中了' + ' ' + key + ' ' + str(record[key]) + ' ' + u'次' + '\n')

    for key, keywords in sorted(express.items(), key=lambda d:d[1], reverse = True):
        f2.write(u'使用了' + ' ' + key + ' ' + u'表情' + ' ' + str(express[key]) + ' ' + u'次' + '\n')

    for key, keywords in sorted(name_set.items(), key=lambda d:d[1], reverse = True):
        f4.write(u'使用了名字' + ' ' + key + ' ' + str(name_set[key]) + ' ' + u'次' + '\n')

    f.close()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
