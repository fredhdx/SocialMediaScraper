# SinaSpider
新浪微博爬虫程序，得到用户微博及点评信息，以及图片。用于创建timeline
latest mod date: 2018-1-12

# 参考 
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)
[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

# 功能设计
1. 读取微博：用户信息、微博内容、转评赞数据 [x]
2. 读取每条微博配图信息：原图 + 组图 [X]
3. 输出微博内容、图片链接[X]
4. 下载所有图片[X]
5. 微博出现关键词分析[X]
6. 分析结果展示[]

# 输出
1. /weibo/user_id/user_id.txt
2. /weibo/user_id/imgref_list.txt
3. /weibo/user_id/img_list.txt
4. /weibo/user_id/images/fromlist/downloaded images

# 技术修正
1. 为每N页面读取添加停顿，避免访问次数过多 [x]
2. 为每个requests添加timeout [x]
3. 使用BeautifulSoup("lxml")避免etree安全性问题 [x]

# 文件
## weibo.py [x]
## utitlities [x]
## config [x]
## analysis [x]
## keywrods [x]
## translate.py []
 
