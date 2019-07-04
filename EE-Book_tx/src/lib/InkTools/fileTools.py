# -*- coding: utf-8 -*-
#!/usr/bin/python

import os,shutil
import sys
import imghdr
reload(sys)
sys.setdefaultencoding('utf8')
#
#
# def mymovefile(srcfile,dstfile):
#     if not os.path.isfile(srcfile):
#         print "%s not exist!"%(srcfile)
#     else:
#         fpath,fname=os.path.split(dstfile)    #分离文件名和路径
#         if not os.path.exists(fpath):
#             os.makedirs(fpath)                #创建路径
#         shutil.move(srcfile,dstfile)          #移动文件
#         print "move %s -> %s"%( srcfile,dstfile)
#
# def mycopyfile(srcfile,dstfile):
#     if not os.path.isfile(srcfile):
#         print "%s not exist!"%(srcfile)
#     else:
#         fpath,fname=os.path.split(dstfile)    #分离文件名和路径
#         if not os.path.exists(fpath):
#             os.makedirs(fpath)                #创建路径
#         shutil.copyfile(srcfile,dstfile)      #复制文件
#         print "copy %s -> %s"%( srcfile,dstfile)
#
#
#
#
#
# if __name__ == "__main__":
#
#      rootdir = '/ink/work/PA/Python_project/ZhihuHelp/Z_back/武侠评论/知乎图片池'
#      list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
#      for i in range(0,len(list)):
#             path = os.path.join(rootdir,list[i])
#             if os.path.isfile(path):
#                 # print  path
#                 srcfile = path
#                 dstfile= u"/ink/work/PA/Python_project/ZhihuHelp/Z_back/知乎电子书临时资源库/知乎图片池/{}".format(path.split('/')[-1])
#
#                 mymovefile(srcfile,dstfile)

if __name__ == "__main__":

     rootdir = '/ink/work/PA/Python_project/ZhihuHelp/知乎电子书临时资源库/知乎图片池/'
     list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
     for i in range(0,len(list)):
            path = os.path.join(rootdir,list[i])
            if os.path.isfile(path):
                # print  path
                srcfile = path
                # print srcfile
                dstfile= u"/ink/work/PA/Python_project/ZhihuHelp/知乎电子书临时资源库/知乎图片池/{}".format(path.split('/')[-1])


                #  清除无法预览的图片
                check = imghdr.what(dstfile)

                if check == None:
                    print dstfile
                    os.remove(dstfile)













