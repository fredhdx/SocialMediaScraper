"""
设置文件
"""

# 微博读取参数
user_id = 5491331848 # 例如：杨冰怡id: 5491331848
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博(包括转)，1代表只爬取用户的原创微博
cookie = {"Cookie":""} # 将your cookie替换成你自己的cookie

# 抓取停顿参数
connection_timeout = 90 # request链接timeout, 秒
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 读取停顿时长,秒

# 图片后缀名
image_format = ['jpg','bmp','jpeg','svg','gif','png','tiff','exif', \
               'JPG', 'BMP','JPEG','SVG','GIF','PNG','TIFF','Exif','WebP']

line_to_buffer = 20 # img_list,每_行写入文件
