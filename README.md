# SinaSpider: A python scrapping package for the Chinese tweeter platform weibo.com

[中文说明](https://github.com/knightReigh/SinaSpider/blob/master/readme-ch.md)
## Intro

Weibo.com is the Chinese tweeter platform used by millions of people. This program helps download all published posts and accompanying images from a selected user, along with statistics such as retweet/like numbers for each post.

This program uses `Python>3.0`, `requests` and `BeautifulSoup` packages, and requires that the user has its own weibo account (so that he/she can obtain a working `cookie`). 

Because weibo.com performs unpredictable updates that changes its page HTML structure, this program might not work properly at some point in the future. In that case, try submit an [issue](https://github.com/knightReigh/SinaSpider/issues).

## Requirement
`Python>3.0, requests, BeautifulSoup`

A weib.com account.

## Functions
1. Obtain user's weibo, obtaining posts, user info, images links, and retweet/likes statistics.

2. Decode direct download links for images.

3. Download images from saved link list.

4. Analyze keywords used by the user

5. Make beautiful timeline web page based on saved posts.

## How to use
### I. Obtain account cookie.

+ Open `weibo.cn`, log into your account (**Not .com, use .cn**).
+ Open browser's web dev tool.
+ Go to *Network* tab, refresh.
+ Click on the *weibo.cn* line; to the right, click *Headers*.
+ Under *Requested headers*, find *Cookie*, copy its content.

### II. Enter your cookie and target user_id

In file `config.py`: enter your copied cookie content and the user_id that you want to scrape.

*Please don't use the same user for both the cookie and the target user_id*
   

### III. Download weibo posts

Use `run_read.py`.

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
4. Bilingual README

# Acknowledgement and Reference
[weiboSpider](https://github.com/knightReigh/weiboSpider-1)

[weiboAnalysis](https://github.com/dingmyu/weibo_analysis)

# Copyright
The program is licensed under [MIT](https://opensource.org/licenses/MIT). 

The script only provides a tool to obtain open, published internet content on weibo.com. Please obtain any necessary permission to use any weibo user's posts content or images, and comply by any copyrights laws. 

The author of this script is not responsible for any act of users or copyright infringement. Please use under your own discretion.
