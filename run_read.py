#!/usr/bin/env python3
import sys
from datetime import datetime
from utilities import stream_tee
from weibo import Weibo
from config import cookie
from config import filter
from config import user_id
from config import connection_timeout
from config import pause_interval
from config import pause_time


# 日志
logname = datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log'
logfile = open(logname,"w+")
sys.stdout = stream_tee(sys.stdout, logfile)

# 读取微博
w = Weibo(user_id,filter)
w.set_cookie(cookie)
w.connection_timeout = connection_timeout
w.pause_interval = pause_interval
w.pause_time = pause_time
w.get_user()
w.get_weibo()

# 输出结果
w.write_txt()
w.write_imgref_list()

# 下载图片,deprecated（请用utilities进行)
"""
通过run_read读取微博并输出：
    1./weibo/user_id/user_id-compact.txt
    2./weibo/user_id/img_list.txt
通过utilities.repair_image_list修复未解析链接
    mv img_list-new.txt img_list.txt
通过utilities.download_from_list开始下载
"""


logfile.close()
