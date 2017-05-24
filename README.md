## python抓取雪球 淘股吧文章
### 雪球使用 
XQHttp.py 文件需要配置你自己的Cookie  也就是header 中’Cookie': 值  xq_a_token 和bid 

ReadList.txt  填写需要抓取的雪球大V 地址 例如：https://xueqiu.com/2733321298
抓取贴子，言论，API说明：
 \_url = "http://xueqiu.com/v4/statuses/user\_timeline.json?user\_id={0}&page={1}&type=2"  2主贴  5 回复 ""为全部
可自行修改，位于xueqiu_workerpy
### 淘股吧
如果TGBHttp.py 中Cookie过期，需要更新，
淘股吧（只发布抓取帖子版，***完整抓取用户所有日志，跟帖不在此发布***）

ReadList.txt配置 帖子地址 例如 龙飞虎 [我相信这个帐号的未来会很灿烂！][1]
 https://www.taoguba.com.cn/Article/175600/0  原贴地址/0 表示默认抓取完全部帖子，原贴地址/x 表示抓取到第x页 ,默认 0 
默认配置 提取主贴 + 点亮 + 捧场 + 作者所有回复 
如需帖子完整版，配置taoguba\_article  解析
 

### after all 
看看人家巴菲特 
其他[知乎助手][1] 抓微信（传送门文章）[山石观市][2]  

[1]:	https://github.com/YaoZeyuan/ZhihuHelp
[2]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%B8%93%E6%A0%8F%E5%B1%B1%E7%9F%B3%E8%A7%82%E5%B8%82(cssstock)%E6%96%87%E7%AB%A0%E9%9B%86.epub

### 程序fork自 [EE-Book][2] [知乎助手][3]
原EE-Book介绍：
# EE-Book

[中文][4] | [English][5]  

[EE-Book][6] 是一个命令行程序，它可以从网络上爬取内容制作成EPub格式电子书。  

网页版 →\_→ [ee-book.org][7]

### 目录
* [支持的网站][8]
* [用法][9]
* [参与进来][10]
* [相关信息][11]
* [感谢][12]
* [License][13]

---

## 支持的网站

| 名称 | 主页                               | 支持类型                          |
| :------ | ---------------------------------------- | ---------------------------------------- |
| 知乎      | [www.zhihu.com][14]    | **问题：** `zhihu.com/question/{question_id}`<br/>**答案：** `zhihu.com/question/{question_id}/answer/{answer_id}`<br/>**话题：** `zhihu.com/topic/{topic_id}`<br/>**用户的全部回答：** `zhihu.com/people/{people_id}` or `zhihu.com/people/{people_id}/answers`<br/>**收藏夹：** `zhihu.com/collection/{collection_id}` <br/> **专栏：** `zhuanlan.zhihu.com/{zhuanlan_id}` |
| 简书      | [www.jianshu.com][15] | **用户的所有文章：** `jianshu.com/users/{people_id}/latest_articles`<br/>**专题：** `jianshu.com/collection/{collection_id}`<br/>**文集：** `jianshu.com/notebooks/{notebooks_id}/latest` or `jianshu.com/notebooks/{notebooks_id}/top` |
| csdn博客  | [blog.csdn.net][16]    | **用户的所有文章：** `blog.sina.com.cn/u/{people_id}` |
| 新浪博客   | [blog.sina.com.cn][17] | **用户的所有文章：** `blog.csdn.net/{people_id}` |
| 博客园     | [www.cnblogs.com][18] | **用户的所有文章：** `cnblogs.com/{people_id}/`  |
| 易百教程   | [www.yiibai.com][19] | **某个教程的文章：** `yiibai.com/{tutorial_kind}`|
| Talk Python To Me | [www.talkpython.fm][20]| **文稿:** `https://talkpython.fm/episodes/all/`|

## 用法

获得帮助信息:  

```bash
$ python ee-book -h
```

举个例子:  

```bash
$ python ee-book -u jianshu.com/users/b1dd2b2c87a8/latest_articles
```

稍等片刻, 你就可以得到电子书了:  

![directory][image-1]  

![scheme][image-2]


## 参与进来

...当然欢迎

### 搭建 EE-Book 的开发环境

```bash
$ pip install -r requirements.txt
```

[安装 pyqt4][21]

### [TODO List][22]


## 相关信息

* 之前版本的 [README][23]

* 发在[v2ex][24]的一篇[文章][25]

## 感谢

* [知乎助手][26]
* [calibre][27]
* [you-get][28]

## License

[MIT license][29].

[1]:	https://www.taoguba.com.cn/Article/175600/1
[2]:	https://github.com/ee-book/EE-Book
[3]:	https://github.com/YaoZeyuan/ZhihuHelp
[4]:	./README.md
[5]:	./README_en.md
[6]:	https://github.com/knarfeh/EE-Book
[7]:	http://ee-book.org
[8]:	#%E6%94%AF%E6%8C%81%E7%9A%84%E7%BD%91%E7%AB%99
[9]:	#%E7%94%A8%E6%B3%95
[10]:	#%E5%8F%82%E4%B8%8E%E8%BF%9B%E6%9D%A5
[11]:	#%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF
[12]:	#%E6%84%9F%E8%B0%A2
[13]:	#license
[14]:	http://www.zhihu.com
[15]:	http://www.jianshu.com
[16]:	http://blog.csdn.net
[17]:	http://blog.sina.com.cn/
[18]:	http://www.cnblogs.com/
[19]:	http://www.yiibai.com/
[20]:	https://www.talkpython.fm
[21]:	https://riverbankcomputing.com/software/pyqt/download/
[22]:	./notes/TODOlist.md
[23]:	https://github.com/knarfeh/EE-Book/blob/c4d870ff8cca6bbac97f04c9da727397cee8d519/README.md
[24]:	https://v2ex.com/
[25]:	http://knarfeh.github.io/2016/03/17/EE-Book/
[26]:	https://github.com/YaoZeyuan/ZhihuHelp
[27]:	https://github.com/kovidgoyal/calibre
[28]:	https://github.com/soimort/you-get
[29]:	./LICENSE

[image-1]:	http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09directory.png
[image-2]:	http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09Scheme.png

