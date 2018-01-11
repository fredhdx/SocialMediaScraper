"""
一些有用的class
"""
import sys
import re
import os
import shutil
import time
import requests
from bs4 import BeautifulSoup

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

def download_image_from_list(filepath,outpath):
    """
    从图片列表下载图片
    输入：path/inputfile (txt,每行: weibo_title, imgurl)
    输出：path/fromlist/
    imgurl要求：http://******/name.jpg/ext
    """
    print("从" + filepath + "列表下载图片")
    if not os.path.isfile(filepath):
        print(filepath + "不存在")
        return None

    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    with open(filepath,"r") as f:
        for line in f:
            if len(line.split("/")[-1].split(".")) <= 1:
                print("无效图片链接: " + line)
                continue

            weibo_title = line.split(",")[0]
            imgurl = line.split(",")[1]
            extension = imgurl[-4:] # .jpg
            temp = outpath + os.path.sep + "fromlist" + os.path.sep + weibo_title + extension
            start_time = time.time()
            while True:
                try:
                    r = requests.get(imgurl,stream=True)
                    break
                except Exception as e:
                    if time.time() > start_time + 90:
                        raise Exception('Unable to get connection %s (download image) after 90 \
                                seconds of ConnectionErrors' % (imgurl))
                    else:
                        time.sleep(1)

            if r.status_code == 200:
                with open(temp,'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw,f)

            print("已下载: %s" % imgurl)
    print("全部图片下载完成: " + outpath + os.path.sep + "fromlist")
