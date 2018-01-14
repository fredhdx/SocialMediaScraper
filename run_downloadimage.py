#!/usr/bin/env python3
from utilities import download_image_from_list
from config import user_id
import os

# base_dir = "/media/dongxu/data1/Python_Directory/weiboSpider/weiboSpider"
# list_path = "weibo/5491331848/imgref_list.txt"

base_dir = os.getcwd()
list_path = "weibo" + os.path.sep + str(user_id) + os.path.sep + "img_list.txt"

download_image_from_list(base_dir + os.path.sep + list_path)
