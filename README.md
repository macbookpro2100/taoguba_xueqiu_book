## python抓取 微信公众号 雪球 文章

Add 微信文章 郭树清，周小川，刘鹤，易纲，埃隆·马斯克，沃伦·巴菲特，贝索斯，孙正义等访谈演讲文章集

![scheme][img_macbookpro2100]

### Tips http://chuansong.me/ 容易被屏蔽，延时要加大
### 2018-8-15 更新 换回ZhihuHelp 爬 [武侠评论][34] [吃瓜群众岱岱][35] [顾子明政事堂][36]  [今天看啥][37] 

微信文章需手动添加列表生成book
股社区 政事堂 吃瓜群众岱   
补充链接:https://pan.baidu.com/s/1869bKc9V1w5n1j10gCepbw  密码:qo0g
感慨时过境迁，bye

## 支持的网站

| 名称 | 主页                               | 支持类型                          |
| :------ | ---------------------------------------- | ---------------------------------------- |
| 武侠评论      | [https://www.wuxiareview.com/][34]    | **用户：** `https://www.wuxiareview.com/category/daidai/{}`<br/>  |
| 传送门      |  http://chuansong.me/ |   **主页：** `http://chuansong.me/account/{}`<br/>  |
| 股社区  |  http://www.gushequ.com/    | **用户的所有文章：** `http://www.gushequ.com/{2018}` |
| 雪球   | https://xueqiu.com/ | **用户的所有文章：** `https://xueqiu.com/u/{id}#{id名称}`|
| 今天看啥     | http://www.jintiankansha.me | **用户的所有文章：** `http://www.jintiankansha.me/column/{id}/#{用户名}#{页数}`  |
| 虎嗅   | https://www.huxiu.com/ | **所有{Seach}：** `https://www.huxiu.com/{}#{}`例如https://www.huxiu.com/华为#36|
| 心声社区   | 华为家事 | **所有内部公开邮件：** `http://huawei.com/2018/` |
| 淘股吧   | 帖子+跟帖 |   https://www.taoguba.com.cn/Article/1483634/1


### 2018-7-20 更新 巴菲特芒格在BerkshireHathaway 历年年股东大会问答Google机器翻译 
来源网址是：https://buffett.cnbc.com/warren-buffett-archive/
 
![scheme][wechat]

### Last 更新虎嗅上 任正非马云马化腾演讲访谈等
add [简书地址][31]  
发布任正非华为讲话集合 心声社区 + 新浪博客整理

多看阅读效果
### 标题
![directory][img-1]  
### 内容
![scheme][img-2]
### 目录
![scheme][img-3]
 

 
 

 
### after all 
看看人家巴菲特 
其他[知乎助手][1] 抓微信（传送门文章）[山石观市][2]  

### 程序fork自 [EE-Book][222] [知乎助手][3]
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

[1]:	https://github.com/YaoZeyuan/ZhihuHelp
[2]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%B8%93%E6%A0%8F%E5%B1%B1%E7%9F%B3%E8%A7%82%E5%B8%82(cssstock)%E6%96%87%E7%AB%A0%E9%9B%86.epub
[222]:	https://github.com/ee-book/EE-Book
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

[31]:	https://www.jianshu.com/p/cc1dc1f8502c

[34]:	https://www.wuxiareview.com/
[35]:	https://www.wuxiareview.com/category/daidai/
[36]:	https://www.wuxiareview.com/category/gzmdzst/
[37]:	http://www.jintiankansha.me/

[image-1]:	http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09directory.png
[image-2]:	http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09Scheme.png

[img-1]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%BB%BB%E6%AD%A3%E9%9D%9E%E9%A9%AC%E4%BA%91%E9%A9%AC%E5%8C%96%E8%85%BE%E2%80%A6%E2%80%A6/r1.jpg
[img-2]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%BB%BB%E6%AD%A3%E9%9D%9E%E9%A9%AC%E4%BA%91%E9%A9%AC%E5%8C%96%E8%85%BE%E2%80%A6%E2%80%A6/r2.jpg
[img-3]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%BB%BB%E6%AD%A3%E9%9D%9E%E9%A9%AC%E4%BA%91%E9%A9%AC%E5%8C%96%E8%85%BE%E2%80%A6%E2%80%A6/r3.jpg

[wechat]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/blob/master/%E4%BB%BB%E6%AD%A3%E9%9D%9E%E9%A9%AC%E4%BA%91%E9%A9%AC%E5%8C%96%E8%85%BE%E2%80%A6%E2%80%A6/ink.jpeg

[img_macbookpro2100]:	https://github.com/macbookpro2100/taoguba_xueqiu_book/tree/master/weChat/macbookpro2100.jpg

