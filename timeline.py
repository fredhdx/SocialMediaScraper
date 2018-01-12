#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
创立一个timeline
template: https://bootsnipp.com/snippets/featured/timeline-21-with-images-and-responsive
"""
import os
import re

class timecard:

    def __init__(self):
        self.time = [] # each: '2018-1-2'
        self.meta = [] # each: {'up_num','retweet_num','comment_num'}
        self.content = [] # each: 'ransfdlsmdkglja'
        self.img_path = [] # each: '/path/to/img.jpg'
        self.img_src = [] # each: 'url-to-jpg'

    def load_text(self,inputfile):
        print("为timecard加载文字信息")
        if not os.path.isfile(inputfile):
            print("文字文件不存在 %s\n加载失败" % inputfile)
            return

        from utilities import read_weibo_file
        weibo = read_weibo_file(inputfile)
        self.time = weibo['publish_time']
        self.content = weibo['content']
        self.meta = weibo['meta']
        self.img_src = [""] * len(self.content)
        self.img_path = [""] * len(self.content)

    def load_img(self,imgfile):
        print("为timecard加载图片超链接")
        if not os.path.isfile(imgfile):
            print("图片文件不存在 %s\n加载失败" % imgfile)
            return

        with open(imgfile,'r') as f:
            for line in f:
                weibo_title = int(line.split(',')[0])
                imgurl = line.split(',')[1]

                # 使用第一张有效图片链接
                if self.img_src[weibo_title - 1] == "" and len(imgurl.split('.')>1):
                    self.img_src[weibo_title - 1] = imgurl

    def load_img_file(self,img_dir):
        print("为timecard加载图片超链接")
        if not os.path.isdir(img_dir):
            print("文件夹不存在 %s" % img_dir)
            return

        from utilities import get_subdir
        from config import image_format

        dirs = get_subdir(img_dir)
        for each_dir in dirs:
            files = [os.path.join(each_dir,f) for f in os.listdir(each_dir) \
                    if os.path.isfile(os.path.join(each_dir,f))]
            files = [f.split(os.path.sep)[-1] for f in files if f.split('.')[-1] in image_format]
            if files:
                weibo_title = int(each_dir.split(os.path.sep)[-2])
                file_path = sorted(files, key=lambda f: int(f.split('.')[-2]))[0]
                self.img_path[weibo_title - 1] = each_dir + os.path.sep + file_path

