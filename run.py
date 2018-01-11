#!/usr/bin/env python3
import sys
from datetime import datetime

user_id = 5621452734
cookie = {"Cookie": "_T_WM=3ee66893b0c9bfd883628d437ccdb644; SCF=Aqt1CGgzsIJiOEI_UrIiVE4sjjLz6YI7JXnoy65qoX5SBDW29c-SHrlkJaigKdSjXpq_F86MXllb7P0_oP55KtM.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvW0Jk66DBo_dquLugAH8g5JpX5K-hUgL.Fo-4S0epSK5cShM2dJLoIEvJi--fiK.7iKn0i--NiKnpi-8Fi--4iK.XiKnfi--NiKLWiKnXi--NiKyhi-8FP7tt; M_WEIBOCN_PARAMS=uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword; SUB=_2A253SuJZDeRhGeNH7FEQ9S7KzzuIHXVUtI4RrDV6PUJbkdBeLWf9kW1NSpoOV0ki5QMBX32mUOLHh_eGthS4LWw8; SUHB=010G4fK5jataN9; SSOLoginState=1515098633"}  # 将your cookie替换成自己的cookie
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博

connection_timeout = 90 # seconds
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 停顿时长 seconds

from utilities import *
logname = datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log'
logfile = open(logname,"w+")
sys.stdout = stream_tee(sys.stdout, logfile)

from weibo import Weibo
w = Weibo(user_id,filter,cookie)

w.connection_timeout = connection_timeout
w.pause_interval = pause_interval
w.pause_time = pause_time

w.get_user()
w.get_weibo()
w.write_txt()
w.decode_image()
w.download_image("all")

logfile.close()
