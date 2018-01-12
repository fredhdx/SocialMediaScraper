#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
所有路径为相对路径
当前目录:
    + weibo.py
    + analysis.py
    + etc
工作目录:
    当前目录/weibo/user_id/
    当前目录/weibo/user_id/images
"""

import os
import re
import requests
import sys
import traceback
import csv
import time
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

class Weibo:

    # 默认爬虫参数
    connection_timeout = 90 # seconds
    pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
    pause_time = 5 # 停顿时长 seconds

    # Weibo类初始化
    def __init__(self, user_id, filter=1, cookie = {"Cookie":""}):
        self.user = {"user_id":user_id,"username":"","sex":"","region":"","birthday":"","intro":""}  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.meta = {"following":0,"followers":0} # 关注数、粉丝数
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.pic_count = 0   # 所含原创图片数
        self.weibo = []  # 微博内容     {"weibo_content":"", "publish_time":"", "up_num":int,"retweet_num":int, "comment_num":int, "imgref":"","imgsetref":""}
                         # 内容，发布时间，赞，转发，评论
        self.imgurl = [] # 解析后微博图片
        self.imgset = [] # 解析后微博组图
        self.cookie = cookie

    def get_user(self):
        # 获取用户信息
        url = "https://weibo.cn/%d/info" % (int(self.user["user_id"]))
        start_time = time.time()
        while True:
            try:
                html = requests.get(url,cookies = self.cookie).content
                break
            except Exception as e:
                if time.time() > start_time + self.connection_timeout:
                    raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")
        self.user["username"] = soup.find("title").text[:-3]
        textual = ''.join(item.text for item in soup.findAll("div",{"class":"c"}))
        self.user["sex"] = re.search(r'性别:(.*)?地区',textual).group(1)
        self.user["region"] = re.search(r'地区:(.*)?生日',textual).group(1)
        self.user["birthday"] = re.search(r'生日:(.*)?简介',textual).group(1)
        self.user['intro'] = re.search(r'简介:(.*)?互联网',textual).group(1)
        print("用户名：" + str(self.user["username"]))

        # 获取用户微博数、关注数、粉丝数
        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user['user_id'], self.filter)
        start_time = time.time()
        while True:
            try:
                html = requests.get(url,cookies = self.cookie).content
                break
            except Exception as e:
                if time.time() > start_time + self.connection_timeout: raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")
        try:
            self.weibo_num = int(soup.find("div",{"class":"tip2"}).find("span",{"class":"tc"}).text[3:-1])
            self.meta["following"] = int(soup.find("div",{"class":"tip2"}).findAll("a")[0].text[3:-1])
            self.meta["followers"] = int(soup.find("div",{"class":"tip2"}).findAll("a")[1].text[3:-1])

            print("微博数：" + str(self.weibo_num))
            print("关注数：" + str(self.meta["following"]))
            print("粉丝数：" + str(self.meta["followers"]))
        except Exception as e:
            print(e)
            traceback.print_exc()

    def get_weibo(self):
        # 读取每条微博信息
        #   分times次读取，中途停顿，避免短时间访问次数过多
        #   文字信息储存于: {"content","pub_time","up_num","retweet_num","comment_num"} @ */weibo/weibo.txt
        #   图片信息储存：*/weibo/pics/index/0.ext + content.txt

        page_num = 1
        pic_count = 0

        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user['user_id'], self.filter)
        start_time = time.time()
        while True:
            try:
                html = requests.get(url,cookies = self.cookie).content
                break
            except Exception as e:
                if time.time() > start_time + self.connection_timeout:
                    raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")

        if soup.find("input",{"name":"mp"}) == None:
            page_num = 1
        else:
            page_num = int(soup.find("input",{"name":"mp"})["value"])

        # 设定读取批次
        pause_interval = self.pause_interval
        pause_num = 1

        for page in range(1,page_num + 1):

            # 周期停顿
            if (page % pause_interval == 0):
                print("正在进行第%d次停顿,防止访问次数过多" % pause_num)
                time.sleep(self.pause_time)
                pause_num += 1

            # 获取页面
            url = "https://weibo.cn/u/%d?filter=%d&page=%d" % (self.user['user_id'],self.filter,page)
            start_time = time.time()
            while True:
                try:
                    html = requests.get(url,cookies = self.cookie).content
                    break
                except Exception as e:
                    if time.time() > start_time + self.connection_timeout:
                        raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                                % (url, self.connection_timeout))
                    else:
                        time.sleep(1)

            soup = BeautifulSoup(html,"lxml")
            info = soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['c'])
            if (len(info)>3):
                if soup.title.text == '我的首页':
                    info = info[2:]
                info = info[:len(info)-2] # 最后两项为设置信息
                for each in info:
                    # 获取每页微博信息
                    str_class = each.find("span")["class"][0]
                    weibo_content = ""
                    publish_time = ""
                    up_num = 0
                    retweet_num = 0
                    comment_num = 0
                    imgref = ""
                    imgsetref = ""

                    # 微博内容
                    if str_class == 'cmt':
                        # 转发了 + 原信息 + 转发理由
                        retweet_from = each.findAll("div")[0].findAll("span")[0].text
                        retweet_content = each.findAll("div")[0].findAll("span")[1].text
                        retweet_cite = each.findAll("div")[-1].text
                        retweet_cite = retweet_cite[:retweet_cite.find(u'赞')]
                        weibo_content = retweet_from + '\n' + retweet_content + '\n' + retweet_cite
                    else:       # str_class == 'ctt'
                        weibo_content = each.find("span",{"class":"ctt"}).text

                    weibo_content = weibo_content.replace(u'\u200b','').replace('\xa0',' ')
                    print("微博内容：" + weibo_content)

                    # 发布时间
                    publish_time = each.findAll("span",{"class":"ct"})[-1].text.split("来自")[0].strip()
                    if "刚刚" in publish_time:
                        publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    elif "分钟" in publish_time:
                        minute = publish_time[:publish_time.find("分钟")]
                        publish_time = (datetime.now() - timedelta(minutes=int(minute))).strftime('%Y-%m-%d %H:%M')
                    elif "今天" in publish_time:
                        today = datetime.now().strftime('%Y-%m-%d')
                        publish_time = today + " " + publish_time[3:]
                    elif "月" in publish_time:
                        publish_time = datetime.now().strftime("%Y") + '-' + publish_time[0:2] \
                                        + '-' + publish_time[3:5] + '-' + publish_time[7:12]
                    else:
                        publish_time = publish_time[:16]
                    print("微博发布时间：" + publish_time)

                    # guid: 转、评、赞
                    str_meta = each.findAll("div")[-1].text
                    str_meta = str_meta[str_meta.find('赞'):]
                    pattern = r"\d+\.?\d*"
                    guid = re.findall(pattern, str_meta, re.M)

                    up_num = int(guid[0])
                    retweet_num = int(guid[1])
                    comment_num = int(guid[2])

                    print("点赞数：" + str(up_num) + \
                            ' 转发数：' + str(retweet_num) + \
                            ' 评论数：' + str(comment_num))
                    print()

                    # 原创图片（如果存在）
                    if str_class == "ctt" or str_class == "kt":
                        tmp_imgurl = each.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
                        if tmp_imgurl:
                            imgref = re.sub(r"amp;", '', tmp_imgurl[0]['href'])

                        tmp_imgseturl = each.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/picAll',re.I))
                        if tmp_imgseturl:
                            imgsetref = tmp_imgseturl[0]['href']

                    # 储存
                    weibo_instance = {"weibo_content":weibo_content,"publish_time":publish_time,"up_num":up_num,"retweet_num":retweet_num,"comment_num":comment_num, "imgref":imgref,"imgsetref":imgsetref}
                    self.weibo.append(weibo_instance)
                    self.weibo_num2 += 1

        self.pic_count = pic_count
        if not self.filter:
            print("共" + str(self.weibo_num) + "条微博")
        else:
            print("共" + str(self.weibo_num) + "条微博,其中" + \
                    str(self.weibo_num2) + "为原创微博")

    # 解析微博图片
    def decode_image(self):
        print("开始解析微博图片")
        start = time.time()
        pic_count = 0
        weibo_count = 1
        urllist_set = set()

        # 写出文件
        basepath = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(self.user['user_id'])
        if not os.path.isdir(basepath):
            os.makedirs(basepath)
        file_path = basepath + os.path.sep + "img_list.txt"

        if os.path.isfile(file_path):
            backup_path = basepath + os.path.sep + "img_list-" + datetime.now().strftime('%Y-%m-%d-%H-%M') + ".txt"
            print("备份 %s > %s" % (file_path.split(os.path.sep)[-1], backup_path.split(os.path.sep)[-1]))
            os.rename(file_path, backup_path)
        f = open(file_path,"w")

        for weibo in self.weibo:
            imgref = weibo['imgref']
            imgsetref = weibo['imgsetref']

            print("正在解析第%d条微博" % weibo_count)
            if imgref:
                start_time = time.time()

                imgurl = imgref
                try_num = 1
                while try_num < 10:
                    while True:
                        try:
                            html = requests.get(imgref,cookies=self.cookie)
                            break
                        except Exception as e:
                            if time.time() > start_time + self.connection_timeout:
                                raise Exception('Unable to get connection %s after %s seconds of ConnectionErrors' \
                                        % (imgref, self.connection_timeout))
                            else:
                                time.sleep(1)
                    if html.url == imgref:
                        soup = BeautifulSoup(html.content,"lxml")
                        imgurl = soup.findAll("a",href=re.compile(r'^http://',re.I))[0]['href']
                    else:
                        imgurl = html.url

                    if imgurl != imgref:
                        break
                    try_num += 1

                self.imgurl.append(imgurl)
                urllist_set.add(imgurl)
                f.write(str(weibo_count) + "," + imgurl + '\n')
                pic_count += 1
                print("封面解析完毕：" + imgurl)
            else:
                print("该微博没有封面图")
                self.imgurl.append("")
            if imgsetref:
                tmp_set = []
                try:
                    html = requests.get(imgsetref,cookies=self.cookie).content
                    soup = BeautifulSoup(html,"lxml")
                    imgurl_set = soup.findAll('a',href=re.compile(r'^/mblog/oripic',re.I))
                    for imgrefpack in imgurl_set:
                        start_time = time.time()

                        try_num = 1
                        imgref = 'http://weibo.cn' + re.sub(r"amp;", '', imgrefpack['href'])
                        imgurl = imgref
                        while try_num < 10:
                            while True:
                                try:
                                    html2 = requests.get(imgref,cookies=self.cookie)
                                    break
                                except Exception as e:
                                    if time.time() > start_time + self.connection_timeout:
                                        raise Exception('Unable to get connection %s after %s seconds of \
                                                ConnectionErrors' % (imgref, self.connection_timeout))
                                    else:
                                        time.sleep(1)
                            if html2.url == imgref:
                                soup2 = BeautifulSoup(html2.content,"lxml")
                                imgurl = soup2.findAll("a",href=re.compile(r'^http://',re.I))[0]['href']
                            else:
                                imgurl = html2.url

                            if imgurl != imgref:
                                break
                            try_num += 1

                        tmp_set.append(imgurl)
                        urllist_set.add(imgurl)
                        f.write(str(weibo_count) + "," + imgurl + '\n')
                        print("已解析：" + imgurl)
                        pic_count += 1
                    self.imgset.append(tmp_set)
                    print("组图解析完毕")
                    time.sleep(self.pause_time)
                except Exception as e:
                    traceback.print_exc()
                    print(e)
            else:
                print("该微博没有组图")
                self.imgset.append([])

            if imgsetref and imgref:
                pic_count -= 1

            print()
            weibo_count += 1

        self.pic_count = pic_count
        end = time.time()
        duration = end - start
        print("完毕. 共耗时%s" % '{:02}:{:02}:{:02}'.format(duration//3600, duration%3600//60, duration%60))
        print("共解析%d条微博, %d张图片" % (weibo_count-1,pic_count))
        print("平均每张耗时: %s" % (duration/pic_count))

        # 保存urllist_set
        f.close()

    # 输出微博内容
    def write_txt(self):
        try:
            if self.filter:
                result_header = "\n\n原创微博内容：\n"
            else:
                result_header = "\n\n微博内容：\n"

            result = ("用户信息\n用户昵称：" + self.user['username'] + \
                      "\n用户id：" + str(self.user['user_id']) + \
                      "\n微博数：" + str(self.weibo_num) + \
                      "\n关注数：" + str(self.meta['following']) + \
                      "\n粉丝数：" + str(self.meta['followers']) + \
                      result_header)

            compact = ""
            compact_count = 1
            for i in range(1, self.weibo_num2 + 1):
                text = (str(i) + ":" + self.weibo[i - 1]['weibo_content'] + "\n" + \
                        "发布时间：" + self.weibo[i - 1]['publish_time'] + "\n" + \
                        "点赞数：" + str(self.weibo[i - 1]['up_num']) + \
                        "	 转发数：" + str(self.weibo[i - 1]['retweet_num']) + \
                        "	 评论数：" + str(self.weibo[i - 1]['comment_num']) + "\n\n")
                result = result + text

                # compact版本用于数据分析，故不计算转发内容
                if re.search(r'^转发.*',self.weibo[i - 1]['weibo_content'], re.M) == None:
                    compact = compact + str(compact_count) + ': ' + \
                            ''.join(self.weibo[i - 1]['weibo_content']) + '\n\n'
                    compact_count += 1

            file_dir = os.getcwd() + os.path.sep + "weibo" + os.path.sep + "%d" % self.user['user_id']
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + os.path.sep + "%d" % self.user['user_id'] + ".txt"
            file_path_c = file_dir + os.path.sep + "%d" % self.user['user_id'] + "-compact.txt"

            if os.path.isfile(file_path):
                backup_path = file_dir + os.path.sep + str(self.user['user_id']) + '-' + \
                        datetime.now().strftime('%Y-%m-%d-%H-%M') + ".txt"
                print("备份 %s > %s" % (file_path.split(os.path.sep)[-1], backup_path.split(os.path.sep)[-1]))
                os.rename(file_path, backup_path)

            if os.path.isfile(file_path_c):
                backup_path_c = file_dir + os.path.sep + str(self.user['user_id']) + '-compact-' + \
                        datetime.now().strftime('%Y-%m-%d-%H-%M') + ".txt"
                print("备份 %s > %s" % (file_path.split(os.path.sep)[-1], backup_path_c.split(os.path.sep)[-1]))
                os.rename(file_path_c, backup_path_c)

            f = open(file_path, "w")
            f2 = open(file_path_c,'w')
            f.write(result)
            f2.write(compact)
            f.close()
            f2.close()
            print("微博写入文件完毕，保存路径:" + file_path)
        except Exception as e:
            print(e)
            traceback.print_exc()

    # 输出imgreflist
    def write_imgref_list(self):
        file_dir = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(self.user['user_id'])
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + os.path.sep + "imgref_list.txt"

        if os.path.isfile(file_path):
            backup_path = file_dir + os.path.sep + "imgref_list-" + datetime.now().strftime('%Y-%m-%d-%H-%M') + ".txt"
            print("备份 %s > %s" % (file_path.split(os.path.sep)[-1], backup_path.split(os.path.sep)[-1]))
            os.rename(file_path, backup_path)

        with open(file_path,'w') as f:
            i = 1
            for each in self.weibo:
                f.write(str(i) + ', ' + each['imgref'] + '\n')
                f.write(str(i) + ', ' + each['imgsetref'] + '\n')
                i += 1

    # 储存图片,默认储存封面图片(single),可选储存所有组图("all")
    def download_image(self,option="single"):
        if len(self.imgurl) == 0 and len(self.imgset) == 0:
            print("object Weibo 图片链接未解析")
            print("............ 请先运行decode_image进行解析")
            return

        print("开始下载微博图片")
        basepath = os.getcwd() + os.path.sep + "weibo" + os.path.sep + "%d" % self.user['user_id']
        image_path = basepath + os.path.sep + "images"
        if not os.path.isdir(image_path):
            os.makedirs(image_path)

        start = time.time()
        weibo_count = 1
        img_count = 0

        for weibo in self.weibo:
            if len(self.imgurl) < weibo_count or len(self.imgset) < weibo_count:
                print("在第%d条微博停止：图片链接未完整解析" % weibo_count)
                break

            if len(self.imgurl[weibo_count - 1])>0 or len(self.imgset[weibo_count - 1])>0:
                print("储存第" + str(weibo_count) + "条微博图片")
                # 为当前微博创立文件夹
                tmp_dir = image_path + os.path.sep + str(weibo_count)
                if not os.path.isdir(tmp_dir):
                    os.makedirs(tmp_dir)
                text_path = tmp_dir + os.path.sep + "content.txt"

                # 下载封面图
                if self.imgurl[weibo_count - 1]:
                    print("找到封面图")
                    imgurl = self.imgurl[weibo_count - 1]
                    if len(imgurl.split("/")[-1].split(".")) <= 1:
                        print("无效图片链接: " + imgurl)
                        continue

                    while True:
                        try:
                            r = requests.get(imgurl,stream=True)
                            break
                        except Exception as e:
                            if time.time() > start_time + self.connection_timeout:
                                raise Exception('Unable to get connection %s (download image )after %s \
                                        seconds of ConnectionErrors' % (imgurl, self.connection_timeout))
                            else:
                                time.sleep(1)

                    extension = imgurl[-4:] # .jpg
                    temp = tmp_dir + os.path.sep + str(weibo_count) + extension
                    if os.path.isfile(temp):
                        print("文件已存在 %s" % temp)
                    elif r.status_code == 200:
                        with open(temp,'wb') as f:
                            for chunk in r.iter_content(chunk_size=512 * 1024):
                                f.write(chunk)

                    print("已下载 %s" % temp)
                    img_count += 1

                # 下载组图
                if option == "all" and len(self.imgset[weibo_count - 1])>0:
                    print("找到组图")
                    x = 1
                    for imgurl in self.imgset[weibo_count - 1]:
                        if len(imgurl.split("/")[-1].split(".")) <= 1:
                            print("无效图片链接: " + imgurl)
                            continue

                        extension = imgurl[-4:] # .jpg
                        temp = tmp_dir + os.path.sep + str(x) + extension

                        start_time = time.time()
                        while True:
                            try:
                                r = requests.get(imgurl,stream=True)
                                break
                            except Exception as e:
                                if time.time() > start_time + self.connection_timeout:
                                    raise Exception('Unable to get connection %s (download image) after %s \
                                            seconds of ConnectionErrors' % (imgurl, self.connection_timeout))
                                else:
                                    time.sleep(1)

                        if os.path.isfile(temp):
                            print("文件已存在 %s" % temp)
                        elif r.status_code == 200:
                            with open(temp,'wb') as f:
                                for chunk in r.iter_content(chunk_size=512 * 1024):
                                    f.write(chunk)
                        print("已下载第%s张图片" % x)
                        img_count += 1
                        x += 1

                f = open(text_path,"w")
                f.write(weibo['weibo_content'])
                f.close()

            weibo_count += 1
            time.sleep(self.pause_time)

        end = time.time()
        duration = end - start
        print("所有图片保存完毕. 共耗时%s" % '{:02}:{:02}:{:02}'.format(duration//3600, duration%3600//60,\
                duration%60))
        print("保存路径:%s" % image_path)

    # 从txt读取微博
    def get_weibo_from_file(self,inputfile):
        """
        路径格式：从当前文件夹开始计算
        默认：/weibo/user_id/user_id.txt
        """
        print("从%s微博文档创立Weibo() object" % inputfile.split(os.path.sep)[-1])

        inputfile = os.getcwd() + os.path.sep + inputfile

        if not os.path.isfile(inputfile):
            print("文件不存在 %s\n读取失败" % inputfile)
            return

        from utilities import read_weibo_file
        file_result = read_weibo_file(inputfile)
        user = file_result['user']
        content = file_result['content']
        time = file_result['publish_time']
        meta = file_result['meta']

        self.user['user_id'] = user['user_id']
        self.user['username'] = user['username']
        self.weibo_num = user['weibo_num']
        self.meta["following"] = user['following']
        self.meta["followers"] = user['followers']

        self.weibo_num2 = len(content)

        for i in range(self.weibo_num2):
            _weibo = {"weibo_content":content[i], "publish_time": time[i], "up_num":meta[i]['up_num'], \
                    "retweet_num":meta[i]['retweet_num'],"comment_num":meta[i]['comment_num'], \
                    "imgref": "", "imgsetref":""}
            self.weibo.append(_weibo)

    # 从imgreflist读取imgref
    def get_imgref_from_file(self,inputfile):
        """
        路径格式：从当前文件夹开始计算
        默认：/weibo/user_id/imgref.txt
        """
        print("从%s读取imgrefs" % inputfile)

        inputfile = os.getcwd() + os.path.sep + inputfile
        if not os.path.isfile(inputfile):
            print("文件不存在 %s\n读取失败" % inputfile)
            return

        img_weibo_count = 0
        with open(inputfile,'r') as f:
            for line in f:
                weibo_title, refurl = line.split(',')
                if re.search(r'^http://weibo.cn/mblog/oripic.*', refurl.strip(), re.I):
                    self.imgref[int(weibo_title) - 1] = refurl.strip()
                    img_weibo_count += 1
                if re.search(r'^http://weibo.cn/mblog/picAll.*', refurl.strip(), re.I):
                    self.imgset[int(weibo_title) - 1] = refurl.strip()
                    img_weibo_count += 1

        print("imgrefs 读取完毕")
        print("共%s条微博，其中%s拥有图片" % (self.weibo_num, img_weibo_count))

    def start(self):
        try:
            self.get_user()
            self.get_weibo()
            self.write_txt()
            self.write_imgref_list()
        except Exception as e:
            print(e)
            traceback.print_exc()
