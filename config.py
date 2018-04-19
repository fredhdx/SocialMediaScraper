"""
设置文件
"""

# 微博读取参数
user_id = 5491331848 # 例如：杨冰怡id: 5491331848
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博(包括转)，1代表只爬取用户的原创微博
cookie = {"Cookie":"_T_WM=54fcd5d6a5c8b82ab086ab1bad601b95; ALF=1526652778; SCF=Ama1IQYsfc4Un6sJdVxQ2yxO7QQewhCh0CosukbQpTKemY0Ew4TK_IwRv_eVjH3f-WCResRWqHB9jZRaFiRvexQ.; SUB=_2A2530yI7DeRhGedM71IR-SfKzzyIHXVVPE5zrDV6PUNbktBeLW7ukW1NWXdlB3xnIKX8csxM-2q4a7KOk4-owyrS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Ih9KL7KYFb2p1hacvLA_J5JpX5KMhUgL.Fo2ESh571K.cSh52dJLoIEMLxK-LB.-LB-H.qPS.i--fiKy2iKLWPEH8SEHFeb-R1HYXP027eh5t; SUHB=0rrq4N5wFZBQoT; SSOLoginState=1524060779"} # 将your cookie替换成你自己的cookie

# 抓取停顿参数
connection_timeout = 90 # request链接timeout, 秒
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 读取停顿时长,秒

# 图片后缀名
image_format = ['jpg','bmp','jpeg','svg','gif','png','tiff','exif', \
               'JPG', 'BMP','JPEG','SVG','GIF','PNG','TIFF','Exif','WebP']

line_to_buffer = 20 # img_list,每_行写入文件
