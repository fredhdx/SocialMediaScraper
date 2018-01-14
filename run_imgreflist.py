#!/usr/bin/env python3
from utilities import decode_imgreflist
from config import user_id
import os

# base_dir = "/media/dongxu/data1/Python_Directory/weiboSpider/weiboSpider"
# list_path = "weibo/5491331848/imgref_list.txt"

base_dir = os.getcwd()
list_path = "weibo" + os.path.sep + str(user_id) + os.path.sep + "imgref_list.txt"

decode_imgreflist(base_dir + os.path.sep + list_path,1)
