import argparse
from weibo import Weibo
import os


def main(filepath):

    w = Weibo(00000,filter=0)
    w.get_weibo_from_file(filepath)
    w.write_csv(filepath.replace("txt", "csv"))



if __name__ == '__main__':

    # open text logging
    parser = argparse.ArgumentParser(description="Update KPI database. -s/Start date, -e/End date")
    parser.add_argument("-f", "--file", type=str, help="filepath")
    args = parser.parse_args()

    main(args.file)


    # /Users/dongxuhuang/devs/SinaSpider/weibo/5462211905/5462211905.txt
