from utilities import save_weibo_file_csv
from config import user_id
import os
import sys
import csv

# user_id = 5491331848

weibo_file = (os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(user_id)
                            + os.path.sep + str(user_id) + '.txt')

if not os.path.isfile(weibo_file):
    print("文件不存在 %s\n读取失败" % weibo_file)
    sys.exit()

save_weibo_file_csv(weibo_file)


