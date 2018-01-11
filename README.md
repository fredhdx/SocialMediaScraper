# SinaSpider
新浪微博爬虫程序，得到用户微博及点评信息，以及图片。用于创建timeline
latest mod date: 2018-1-11

# 参考 
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)
[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

# 功能设计
1. 使用requests & lxml.etree读取微博页面数 [x]
2. 使用requets & lxml.etree读取原创及转发微博内容 [x]
3. 使用xpath分析每条微博点赞，转发及评论数据 [x]
4. 使用requests得到图片信息并下载 [x]

# 输出
1. weibo/user_id.txt (所有微博数据）[x]
2. weibo/user_id-compact.txt (精简原创微博,用于分析) [x]
2. weibo/user_id.csv (表格数据) []
3. weibo/all/weibo_num/content.txt + pictures [x]
4. weibo/analysis/bar chart, pie chart, etc []

# 技术修正
1. 为每N页面读取添加停顿，避免访问次数过多 [x]
2. 为每个requests添加timeout [x]
3. 使用BeautifulSoup("lxml")避免etree安全性问题 [x]

# 文件
## weibo.py: weibo() class definition
    finished  
## translate.py: google translate API
    to do
## analysis.py: keywords, expression, names frequency count, provided by [dingmyu/weibo_analysis](https://github.com/dingmyu/weibo_analysis)
    finished
## keywords.py: store keyword dictionary for analysis: keywords library, provided by [dingmyu/weibo_analysis](https://github.com/dingmyu/weibo_analysis)
    finished
## cookie.py: store cookie information and user_id: configuration data file
    renamed: run.py
 
