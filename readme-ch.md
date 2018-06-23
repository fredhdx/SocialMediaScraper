# 微博爬虫: 微博内容及图片下载

## 介绍
下载微博用户内容和图片。

## 系统要求
`Python>3.0, requests, BeautifulSoup`

## 功能设计
1. 下载微博：用户信息、微博内容、转评赞数据 [x]
2. 读取每条微博配图信息：原图 + 组图 [X]
3. 下载所有图片[X]
4. 微博出现关键词分析[X]
5. 生成时间线网页[X]

## 使用方法
### I. 取得你自己的微博账户cookie

+ 打开 `weibo.cn`, 登录你的账户 (**请使用 .cn，而不是 .com**)
+ 打开浏览器开发工具
+ 点击 *Network* 区块, 刷新网页
+ 点击包含 *weibo.cn* 的行; 点击行右侧 *Headers*
+ 找到 *Requested headers*, 找到 *Cookie*, 复制内容

### II. 输入你的cookie和想要下载的微博id

打开文件 `config.py`: 输入你的cookie和目标微博id

*请不要使用同一微博id获取cookie*
   

### III. 下载微博文字内容

运行 `run_read.py`

++++ 未完待续。。。 +++++

This file will use your cookie to access weibo.cn (mobile version) by mimicing internet request. The file will read user_id's user profile first, then all posts content by reverse chronological order (newest first).

Output files are: `user_id.txt`, `user_id-compact.txt`, `imgref_list.txt`. They are located at `/weibo/user_id/` directory.

+ `user_id.txt` contains user profile info and weibo posts. Each post contains post content and retweet/like statistics and ordered in reverse chronological order.
+ `user_id-compact.txt` contains posts content only, in the same order.
+ `imgref_list.txt` contains each post's image *reference url*, which is used by weibo.com to locate the actual image url. They are stored in the same order as post. If multiple images are present for one post, a *group reference url* is used.

### IV. Decode image reference urls (OPTIONAL)

*The image downloading process is separated into 3 scripts because they all take a long time. It is easier to continue working and debugging with small steps. Because weibo.com saves images at different servers, some image links could not be obtained.* 

Use `run_imgreflist.py`.

This script browses through every *reference url* stored in `imgref_list.txt` and tries to decode it by making a http post to weibo.com's server. The decoded *direct download link* is stored in `img_list.txt` in the same order. If the http post times out, the *reference url* will be stored anyway to reserve the correct order. 

If *group reference link* is found, the script will try to decode all images under this group link. The program does not check the completion of gorup decoding however.

Output file: `img_list.txt`

`img_list.txt` will be stored at `\weibo\user_id`.

#### Continue decoding

It is possible to manually continuing decoding process if the script hangs after long execution time.

To do that:

+ Edit file `run_imgreflist.py`.
+ Find the line `decode_imgreflist(base_dir + os.path.sep + list_path, 1)`. Change the last number to the last recorded index number in `img_list.txt`.
+ Save and quit.
+ Run `run_imgreflist.py` again.

A new `img_list.txt` file will be created; the previous file will be renamed with datetime (for example: `img_list-20180101.txt`).

+ After completion of decoding all reference urls, combine all `img_list-.txt` files in reverse chronological order.

### V. Download images (OPTIONAL)

1. Check `img_list.txt`

Now you have `img_list.txt` that is supposed to contain all *direct download links* for each image from all posts. But some of the direct links might still be *reference links* (a timeout remedy issue). In this case, run `run_fix.py`, which basically go through all links and re-decode any reference urls.

This operation will create `img_list-new.txt`. Rename it to `img_list.txt`. I did not do that automatically because you might want to check the files before starting downloads.

2. Run `run_downloadimage.py`

This script will download images from *direct download links* contained in `img_list.txt`

Images are stored at `/weibo/user_id/images/fromlist/`. Every post will have its own folder named with its index (used in `user_id.txt`).

*Continue download* is supported. Just run this script again. Downloaded images will be skipped automatically.


### VI. Generate timeline web page

Run `run_timeline.py`. This script extracts all posts content and their statistics, and generate a HTML timeline with css. The timeline uses template saved in `\timeline_template\`. You can change the script to use your own template. For more information, read the script.


## Complete list of output files
1. `/weibo/user_id/user_id.txt` (contains all user info and posts)
2. `/weibo/user_iduser_id-compact.txt` (contains compacted posts only)
3. `/weibo/user_id/imgref_list.txt` (contains image reference links)
4. `/weibo/user_id/img_list.txt` (contains image direct download links)
5. `/weibo/user_id/images/fromlist/downloaded images/` (contians image files)

# Changelog (2018.06.23)
1. Add pauses after every N page read for polite web scraping
2. Add timeout exception handler
3. Use BeautifulSoup insdead of lxml for better security
4. Bilingual READ.ME

# Acknowledgement and Reference
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)

[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

**Please make sure that you have read/write permission for working directory**
**请确保所有.py文件在同一目录下且当前用户拥有文件系统读写权限**


# Copyright
The program is licensed under [MIT](https://opensource.org/licenses/MIT). 

The script only provides a tool to obtain open, published internet content on weibo.com. Please obtain any necessary permission to use any weibo user's posts content or images, and comply by any copyrights laws. 

The author of this script is not responsible for any act of users or copyright infringement. Please use under your own discretion.
