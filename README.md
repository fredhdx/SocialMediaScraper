# SinaSpider 创建计划
新浪微博爬虫程序，得到用户微博及点评信息，以及图片。用于创建timeline

#参考 
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)
[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

# 功能设计
1. 使用requests & lxml.etree读取微博页面数
2. 使用requets & lxml.etree读取原创及转发微博内容
3. 使用xpath分析每条微博点赞，转发及评论数据
4. 使用requests得到图片信息并下载

# 输出
1. weibo/user_id.txt (所有微博数据）
2. weibo/user_id.csv (表格数据)
3. weibo/all/weibo_num/content.txt + pictures
4. weibo/analysis/bar chart, pie chart, etc

# 技术修正
1. 为每N页面读取添加停顿，避免访问次数过多
2. 为每个requests添加timeout

# 文件、方程分割
## weibo.py
  + spider()
      + get_page_num()
      + iterate over pages/times
      + get text content
      + get zan/retweet/comment meta
   + get_image()
   + save_bundle()
      + check & create weibo/all/weibo_num
      + save content.txt
      + save image/images with 1,2,3,4,etc.extension
      
 ## translate.py
    + translate() using google translation api
  
  
 ## analysis.py
    + analysis()
 
 ## keywords.py: store keyword dictionary for analysis
 
 ## cookie.py: store cookie information and user_id
 
 ## class.py
    + weibo() class definition
