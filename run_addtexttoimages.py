#!/usr/bin/env python3
from utilities import create_picText
from config import user_id
import os

# base_dir = "/media/dongxu/data1/Python_Directory/weiboSpider/weiboSpider"
# list_path = "weibo/5491331848/imgref_list.txt"

working_path = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(user_id)
create_picText(working_path, user_id)
