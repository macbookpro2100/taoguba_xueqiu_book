<!--title 排序-->


<!--封面 -->

<!--帖子头 -->
<!--跟帖 -->

获取帖子名称除去特殊字符 

book info with 帖子链接 book  info 修复
修复 网页链接 

制作完成 move to XueQiu/Ink

// 雪球最后edit time 




class   pc_p_nr
list_pcyc_l_ = tgo.find_all('div', class_="left pcyc_l")
for tgo_tgo_ in list_pcyc_l_:
    list_zkzz = tgo_tgo_.findAll(name='a',attrs={"href":re.compile(r'^javascript:')})
    for zkzz in list_zkzz:
        zkzz.clear()
