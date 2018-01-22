#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
一些有用的class和function: 所有路径为绝对路径
    + stream_tee(object): 日志记录
    + get_subdir(): 获取子文件夹列表
    + decode_imgurl(url, cookie): 解析微博imgref url
    + download_image_from_list: 从图片链接列表下载图片, 储存在user_id/images/fromlist/
    + repair_image_list(imglist_file): 修复图片链接列表中未解析链接

"""
import re
import os
import time
import requests
import traceback
from bs4 import BeautifulSoup
from config import cookie
from config import pause_time
from config import line_to_buffer
from datetime import datetime

class stream_tee(object):
    # from: http://www.tentech.ca/2011/05/stream-tee-in-python-saving-stdout-to-file-while-keeping-the-console-alive/
    # Based on https://gist.github.com/327585 by Anand Kunal
    def __init__(self, stream1, stream2):
        self.stream1 = stream1
        self.stream2 = stream2
        self.__missing_method_name = None # Hack!

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        self.__missing_method_name = name # Could also be a property
        return getattr(self, '__methodmissing__')

    def __methodmissing__(self, *args, **kwargs):
            # Emit method call to the log copy
            callable2 = getattr(self.stream2, self.__missing_method_name)
            callable2(*args, **kwargs)

            # Emit method call to stdout (stream 1)
            callable1 = getattr(self.stream1, self.__missing_method_name)
            return callable1(*args, **kwargs)

def get_subdir(current_directory):
    dirs = [x[0] for x in os.walk(current_directory)]
    dirs = dirs[1:] # 第一项是current_directory

    # 数字目录排序
    # sorted([int(x.split(os.path.sep)[-1]) for x in dirs])
    # max([int(x.split(os.path.sep)[-1]) for x in dirs])

    return dirs

def decode_imgurl(imgref,cookie):
    connection_timeout = 90
    try_num = 1
    imgurl = imgref

    start_time = time.time()
    while imgurl == imgref:
        while True:
            try:
                html = requests.get(imgref,cookies=cookie, timeout=60)
                break
            except Exception:
                if time.time() > start_time + connection_timeout:
                    raise Exception('Unable to get connection %s after %s seconds of ConnectionErrors' \
                            % (imgref, self.connection_timeout))
                else:
                    time.sleep(1)

        if html.url == imgref:
            soup = BeautifulSoup(html.content,"lxml")
            try:
                imgurl = soup.findAll("a",href=re.compile(r'^http://',re.I))[0]['href']
            except IndexError: # 读取过快导致未能读取网页，重新读取
                print("读取过快")
                imgurl = imgref
                time.sleep(1)
        else:
            imgurl = html.url

        try_num += 1

        if try_num > 10:
            print("解析失败.已达到最大尝试数10. 请手动解析")
            return ""

    print("解析成功: %s" % imgurl)
    return imgurl

def download_image_from_list(filepath,start_position=1):
    """
    从图片列表下载图片
    输入：path/inputfile (txt,每行: weibo_title, imgurl)
    输出：path/fromlist/
    imgurl要求：http://******/name.jpg/ext
    start_position:从第几条微博开始, 避免重复解析
    """
    print("从" + filepath + "列表下载图片")
    if not os.path.isfile(filepath):
        print(filepath + "不存在")
        return None

    outpath = os.path.sep.join(filepath.split(os.path.sep)[:-1]) + \
            os.path.sep + "images" + os.path.sep + "fromlist"
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    # 假设文件名遵从 /weibo/user_id/img_list.txt
    # user_id = int(filepath.split(os.path.sep)[-2])

    subdirs = get_subdir(outpath)
    if subdirs:
        start_position = max([int(x.split(os.path.sep)[-1]) for x in subdirs])
    else:
        start_position = start_position

    weibo_pic_count = 1
    pre_weibo_title = 1
    with open(filepath,"r") as f:
        for line in f:

            weibo_title = line.split(",")[0].strip()
            imgurl = line.split(",")[1].strip()

            if int(weibo_title) >= start_position:

                if len(imgurl.split("/")[-1].split(".")) <= 1:
                    print("无效图片链接: %s" % imgurl)
                    if re.search(r'^https://.*',imgurl,re.I):
                        print("重新解析")
                        imgurl = decode_imgurl(imgurl,cookie)
                        if not imgurl:
                            weibo_pic_count += 1
                            continue
                    else:
                        weibo_pic_count += 1
                        continue

                extension = imgurl[-4:] # .jpg

                if pre_weibo_title != weibo_title:
                    weibo_pic_count = 1 # reset
                    pre_weibo_title = weibo_title
                    time.sleep(1)

                temp_dir = outpath + os.path.sep + weibo_title
                if not os.path.isdir(temp_dir):
                    os.makedirs(temp_dir)
                temp = temp_dir + os.path.sep + str(weibo_pic_count) + extension
                weibo_pic_count += 1

                not_connected = False
                start_time = time.time()
                while True:
                    try:
                        r = requests.get(imgurl,stream=True)
                        break
                    except Exception as e:
                        if time.time() > start_time + 90:
                            not_connected = True
                            raise Exception('Unable to get connection %s (download image) after 60 \
                                    seconds of ConnectionErrors.跳过' % (imgurl))
                        else:
                            time.sleep(1)

                if not_connected:
                    continue
                elif r.status_code == 200:
                    if not os.path.isfile(temp):
                        with open(temp,'wb') as f:
                            for chunk in r.iter_content(chunk_size=512 * 1024):
                                f.write(chunk)
                        print("已下载: %s, %s, %s" % (weibo_title, weibo_pic_count-1,imgurl))
                    else:
                        print("文件已存在: %s, %s, %s" % (weibo_title, weibo_pic_count-1,imgurl))

    print("全部图片下载完成: " + outpath)

def repair_image_list(filepath):
    """
    修复图片中未解析链接
    输入：path/inputfile (txt,每行: weibo_title, imgurl)
    输出: path/inputfile-new
    """
    print("列表: " + filepath)
    if not os.path.isfile(filepath):
        print(filepath + "不存在")
        return None

    outpath = os.path.sep.join(filepath.split(os.path.sep)[:-1])
    filename = filepath.split(os.path.sep)[-1]
    newname = outpath + os.path.sep + filename.split('.')[0] + "-new." + filename.split('.')[-1]

    # 假设文件名遵从 /weibo/user_id/img_list.txt
    # user_id = int(filepath.split(os.path.sep)[-2])

    fo = open(newname,"w")
    line_count = 1
    with open(filepath,"r") as f:
        for line in f:
            weibo_title = line.split(",")[0].strip()
            imgurl = line.split(",")[1].strip()
            if len(imgurl.split("/")[-1].split(".")) <= 1:
                print("无效链接: %s, %s" % (weibo_title,imgurl))
                newurl = decode_imgurl(imgurl,cookie)
                if newurl:
                    imgurl = newurl
                    print("重新解析: %s, %s" %(weibo_title, imgurl))
            else:
                print("%s, %s" % (weibo_title, imgurl))
            fo.write(weibo_title + ", " + imgurl + "\n")
            line_count +=1

    fo.close()

def reformat_time(time_string):
    if len(time_string) >= 16:
        year = time_string[:4]
        month = time_string[5:7]
        day = time_string[8:10]
        hour = time_string[11:13]
        minute = time_string[14:16]
        return year + month + day + hour + minute
    else:
        return time_string

def read_weibo_file(inputfile):
    try:
        f = open(inputfile,'rt', encoding='utf-8')
    except Exception as e:
        print(e)

    last_line = ""

    # 用户信息
    next(f) # 用户信息
    username = next(f)[5:]
    user_id = int(next(f)[5:])
    weibo_num = int(next(f)[4:])
    following = int(next(f)[4:])
    followers = int(next(f)[4:])
    next(f)
    next(f)

    user = {"username":username,"user_id":user_id,"weibo_num":weibo_num,"following":following,"followers":followers}
    content = []
    meta = []
    publish_time = []

    weibo_num = 0
    weibo_content = ""
    for line in f:
        if line != '\n':
            if re.search(r'^发布时间.*',line):
                publish_time.append(reformat_time(line[5:].strip()))
            elif re.search(r'^点赞数.*',line):
                pattern = r"\d+\.?\d*"
                guid = re.findall(pattern,line,re.S | re.M)
                up_num = int(guid[0])
                retweet_num = int(guid[1])
                comment_num = int(guid[2])
                meta.append({"up_num":up_num,"retweet_num":retweet_num,"comment_num":comment_num})
            else:
                weibo_content = weibo_content + line
        else:
            content.append(weibo_content)
            weibo_content = ""
            weibo_num += 1

        # 检查空集
        if len(content) < weibo_num:
            content.append("")
        if len(meta) < weibo_num:
            meta.append({"up_num":0,"retweet_num":0,"comment_num":0})
        if len(publish_time) < weibo_num:
            publish_time.append("2088-12-12 12:12")

    last_line = line

    # 补全不完全信息
    if last_line != '\n':
        weibo_num = weibo_num + 1
        if len(content) < weibo_num:
            content.append("")
        if len(meta) < weibo_num:
            meta.append({"up_num":0,"retweet_num":0,"comment_num":0})
        if len(publish_time) < weibo_num:
            publish_time.append("2088-12-12 12:12")

    return {"user":user,"content":content,"publish_time":publish_time,"meta":meta}

def decode_imgreflist(inputfile,start_position=1):
    if not os.path.isfile(inputfile):
        print("文件不存在 %s" % inputfile)
        return

    # 写出文件
    print("解析imgref列表：" + inputfile.split(os.path.sep)[-1])
    outpath = os.path.sep.join(inputfile.split(os.path.sep)[:-1])
    file_path = outpath + os.path.sep + "img_list.txt"

    if os.path.isfile(file_path):
        backup_path = outpath + os.path.sep + "img_list-" + datetime.now().strftime('%Y-%m-%d-%H-%M') + ".txt"
        print("备份 %s > %s" % (file_path.split(os.path.sep)[-1], backup_path.split(os.path.sep)[-1]))
        os.rename(file_path, backup_path)

    fo = open(file_path,"w",line_to_buffer)
    img_weibo_count = 0
    img_count = 0
    with open(inputfile,'r') as f:
        for line in f:
            if line.strip():
                weibo_title, refurl = line.split(',')
                if int(weibo_title) >= start_position:
                    if re.search(r'^http://weibo.cn/mblog/oripic.*', refurl.strip(), re.I):
                        imgref = refurl.strip()
                        if imgref:
                            print("正在解析第%d条微博原图" % int(weibo_title))
                            newurl = decode_imgurl(imgref,cookie)
                            if newurl:
                                print("已解析")
                                fo.write(weibo_title + ', ' + newurl + '\n')
                                img_count += 1
                            img_weibo_count += 1
                    elif re.search(r'^http://weibo.cn/mblog/picAll.*', refurl.strip(), re.I):
                        imgsetref = refurl.strip()
                        if imgsetref:
                            print("正在解析第%d条微博组图" % int(weibo_title))
                            try:
                                html = requests.get(imgsetref,cookies=cookie).content
                                soup = BeautifulSoup(html,"lxml")
                                imgurl_set = soup.findAll('a',href=re.compile(r'^/mblog/oripic',re.I))
                                total_pics = len(imgurl_set)
                                set_count = 1
                                for imgrefpack in imgurl_set:
                                    imgref = 'http://weibo.cn' + re.sub(r"amp;", '', imgrefpack['href'])
                                    newurl = decode_imgurl(imgref,cookie)
                                    if newurl:
                                        print("已解析组图第%d条/共%d条" % (set_count, total_pics))
                                        fo.write(weibo_title + ', ' + newurl + '\n')
                                        set_count += 1
                                        img_count += 1
                                img_weibo_count += 1
                                time.sleep(pause_time)
                            except Exception as e:
                                traceback.print_exc()
                                print(e)

    fo.close()
    print("所有链接解析完毕")
    print("共%d条配图微博，共%d张图片" % (img_weibo_count,img_count))
    print("储存于: " + file_path)
