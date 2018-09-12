#coding=utf-8
import re
import os,os.path
import shutil

BOUNDARY = u"==========\n" #分隔符
intab = "\/:*?\"<>|"
outtab = "  ： ？“《》 "     #用于替换特殊字符

HTML_HEAD = '''
<!DOCTYPE html>
<html><meta charset="UTF-8">
<head>
    <title>kindle note</title>
    <link rel="stylesheet" href="https://unpkg.com/purecss@1.0.0/build/pure-min.css" 
    integrity="sha384-nn4HPE8lTHyVtfCBi5yW9d20FjT8BJwUXyWZT9InLYax14RDjBj46LmSztkmNP9w" crossorigin="anonymous">
    <link rel="stylesheet" href="style/my.css">
</head>
'''
BOOK_HEAD='''
<!DOCTYPE html>
<html><meta charset="UTF-8">
<head>
    <title>kindle note</title>
    <link rel="stylesheet" href="https://unpkg.com/purecss@1.0.0/build/pure-min.css" 
    integrity="sha384-nn4HPE8lTHyVtfCBi5yW9d20FjT8BJwUXyWZT9InLYax14RDjBj46LmSztkmNP9w" crossorigin="anonymous">
    <link rel="stylesheet" href="../style/my.css">
</head>
'''

HEAD_ELSE = '''
<div class="pure-g">
    <img class="pure-img" src="back.jpg">
</div>
<div>
    <h1 class="header">笔记</h1>
</div> 
'''
BOOK_HEAD_ELSE='''
<div class="pure-g">
    <img class="pure-img" src="../back.jpg">
</div>
'''

END_ELSE = '''
</body>   
</html>
'''

BOOK_NAME = '''
<body>
<div class="header">
        <h1>BookName</h1>
</div>
'''

SENTENCE_CONTENT = '''
<div class="pure-g">
        <div class="pure-u-1-8"></div>
        <div class="pure-u-3-4">
            <h2 class="content">SENTENCE_TXT</h2>
        </div>
        <div class="pure-u-1-8"></div>
</div>
'''
GRID_BEGIN = '''
<div class="pure-g">
    <div class="pure-u-1-8"></div>
    <div class="pure-u-3-4">
            <div class="pure-menu custom-restricted-width">                
                    <ul class="pure-menu-list">
'''

GRID_END = '''
                    </ul>
                </div>
            </div>
    <div class="pure-u-1-8"></div>
</div>
'''

ITEM_CONTENT = '''
<li class="pure-menu-item"><a href="HTML_URL" class="pure-menu-link">HTML_FILE_NAME</a></li>
'''

# 替换不能用作文件名的字符
def changechar(s):
    return s.translate(str.maketrans(intab,outtab))

# 处理sentence列表的方法函数
def getAddr(s):  #获取标注位置
    g = s.split(" | ")[0]
    return g
def getTime(s):  #获取添加时间
    g = s.split(" | ")[1]
    return g.split("\n\n")[0]
def getMark(s):  #获取标注内容
    g = s.split(" | ")[1]
    try:
        return g.split("\n\n")[1]
    except IndexError:
        #print("list index out of range due to empty content")
        return "empty content"

# 分割函数实现利用关键词进行简单的分割成列表
# 结果为每一条单独的笔记，包含书名，时间，位置和内容
f = open("My Clippings.txt", "r", encoding='utf-8')
content = f.read()  # 读取全部内容
content = content.replace(u'\ufeff', u'') #替换书名前的空格
clips = content.split(BOUNDARY)
print("列表个数：",clips.__len__()) # 获取列表的个数
sum = clips.__len__()

# 获取书名存储为列表books，获取除书名外的内容为sentence
both = []  #完整内容。格式为[['',''],['','']……]
books = [] #书名列表
sentence = []  #标注内容
for i in range(0,sum):
    book = clips[i].split("\n-")
    both.append(book)
    if (book != ['']): # 如果书名非空
        books.append(changechar(book[0])) #添加书名，替换特殊字符，以便创建文件
        sentence.append(book[1])          #添加笔记
print('笔记总数：',sentence.__len__())

# 去除书名列表中的重复元素
nameOfBooks = list(set(books))
nameOfBooks.sort(key=books.index)
print('书籍总数：',nameOfBooks.__len__())

# 根据不同书名建立网页文件
stceOfBookCnt = {}   # 记录每本书有几条标注的字典
if os.path.exists('books'):
    shutil.rmtree('books')
    print('rm books dir succ')
os.mkdir('books') #创建一个books目录，用于存放书名网页文件
os.chdir('books') #更改工作目录
for j in range(0,nameOfBooks.__len__()):
    '''
    # 文件名中含有特殊字符则不成创建成功，包括\/*?<>|字符
    '''
    # 网页文件的字符长度不能太长，以免无法在linux下创建
    if nameOfBooks[j].__len__() > 80:
        nameOfBooks[j] = nameOfBooks[j][0:80]  # 截取字符串

    f = open(nameOfBooks[j]+".html",'w',encoding='utf-8') # 创建网页文件
    f.write(BOOK_HEAD)   # 写入html头文件
    f.write(BOOK_HEAD_ELSE)
    f.write(BOOK_NAME.replace('BookName',nameOfBooks[j])) #写入书名
    f.close()
    stceOfBookCnt.__setitem__(nameOfBooks[j],0)  # 清零每本书的标注数量

# 向文件添加标注内容
stce_succ_cnt = 0  # 向html文件添加笔记成功次数
stce_fail_cnt = 0  # 向html文件添加笔记失败次数
file_list = os.listdir(".") # 获取当前目录文件名，存放于file_list
for j in range(0,sentence.__len__()):
    temp = both[j]
    filename = changechar(temp[0][0:80])
    if (filename+".html" in file_list ): # 检索字典
        s = getMark(temp[1])  # 获取标注内容
        f = open(filename+".html",'a',encoding='utf-8') # 打开对应的文件
        if (s != '\n'):       # 如果文本内容非空
            stce_succ_cnt += 1
            cnt_temp = stceOfBookCnt[filename]
            stceOfBookCnt[filename] = cnt_temp+1
            f.write(SENTENCE_CONTENT.replace("SENTENCE_TXT","* "+s))
        else:
            stce_fail_cnt += 1
            print("empty txt",stce_fail_cnt,filename)
        f.close()
    else:
        print("can't find filename html :",temp[0]+".html")
print("sentence add succ cnt = ",stce_succ_cnt)
print("sentence add fail cnt = ",stce_fail_cnt)


#向文件添加脚标
file_list = os.listdir(".") #获取当前目录文件名，存放于file_list
html_count = file_list.__len__()
print("file_list_count",html_count)
for i in range(0,file_list.__len__()):
    '''
    检查文件名是否过长，验证上面的修改是否成功
    '''
    f = open(file_list[i],'a',encoding='utf-8') #打开对应的文件
    f.write(END_ELSE)
    f.close()

#处理index.html
os.chdir("../")
f=open("index.html",'w',encoding='utf-8') #打开对应的文件
f.write(HTML_HEAD.replace("../",""))      #写入html头内容
f.write(HEAD_ELSE.replace("../index.html","#"))
f.write(GRID_BEGIN)
for i in range(0,html_count):
    html_url = "books/"+file_list[i]
    html_name = file_list[i].replace(".html",'')
    f.write(ITEM_CONTENT.replace("HTML_URL",html_url)
                        .replace("HTML_FILE_NAME",html_name)) # 写入本书标注数量
f.write(GRID_END)
f.write(END_ELSE)
f.close()