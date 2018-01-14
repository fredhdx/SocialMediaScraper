# SinaSpider
新浪微博爬虫程序，得到用户微博及点评信息，下载所有配图。

## 参考 
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)
[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

## 功能设计
1. 读取微博：用户信息、微博内容、转评赞数据 [x]
2. 读取每条微博配图信息：原图 + 组图 [X]
3. 输出微博内容、图片链接[X]
4. 下载所有图片[X]
5. 微博出现关键词分析[X]
6. 分析结果展示[]

## 输出
1. /weibo/user_id/user_id.txt
2. /weibo/user_id/imgref_list.txt
3. /weibo/user_id/img_list.txt
4. /weibo/user_id/images/fromlist/downloaded images 

## 技术修正
1. 为每N页面读取添加停顿，避免访问次数过多 [x]
2. 为每个requests添加timeout [x]
3. 使用BeautifulSoup("lxml")避免etree安全性问题 [x]

# 使用方法啦啦啦～
0. 请确保所有.py文件在同一目录下且当前用户拥有文件系统读写权限
1. 在config.py输入自己的微博cookie, 读取目标用户id（获取cookie请阅读[这里])
2. 运行`run_read.py` 读取微博信息，输出 `/weibo/user_id/`:user_id.txt + user_id-compact.txt + imgref_list.txt
    + user_id.txt是所有微博信息(包含用户信息，微博内容，发布时间，点赞转评赞数据)
    + user_id-compact.txt是纯粹微博内容(每一行为一条微博)
    + imgref_list.txt是每条微博配图链接（未解析），如没有则为空行
3. 运行`run_imgreflist.py`解析所有配图链接,输出img_list.txt。如果img_list.txt已存在，建立img_list-日期.txt备份。
    + 如果因为运行太久停顿，请打断程序，已解析内容仍然会被储存在img_list.txt里
    + 打断之后可再次运行，修改`decode_imgreflist(base_dir + os.path.sep + list_path,1)`第二位数值为已解析img_list.txt最后一行的微博计数(`324, http://....../1.jpg`)。程序将从此微博数开始继续解析，生成新的img_list.txt。旧的list将被备份。
    + 解析结束后合并所有img_list即可 (`cat oldest.txt old.txt img_list.txt > img_list-new.txt; mv img_list-new.txt img_list.txt`)
4. 运行`run_fix.py`修复img_list.txt未被成功解析的链接,生成img_list-new.txt。请重命名为img_list.txt。(我也不知道为什么第三步不能全部解析成功，欢迎debug...)
5. 运行`run_downloadimage.py`开始下载图片。图片被储存在`/weibo/user_id/images/fromlist/`。每条微博一个文件夹。
    程序支持断点续传，无需改变任何代码。打断后继续运行就可以了。

**请在任务完成前不要改变生成文件的位置，否则imgref_list.txt和img_list.txt将无法被找到，需要重新解析。**

大概就是这样～其他功能还在开发中，欢迎建议。
