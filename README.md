# 使用爬虫自建简单的视频集合站


### 写在前面
  在本篇教程中，我们将学习如何使用python爬虫来爬取直播平台上的各种信息，并且将其制作成我们自己的视频聚合站。本文参考至伯乐在线，本人复现后制作本篇教程，感谢原博主对项目的开源。
[原文链接](http://python.jobbole.com/88188)

完成本项目你可能需要的基础：[Django](http://www.runoob.com/django/django-tutorial.html)  [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
 [正则表达式](http://www.runoob.com/regexp/regexp-syntax.html) [HTML相关知识](http://www.runoob.com/html/html-tutorial.html)   [leancloud](https://leancloud.cn/docs/leanstorage_guide-python.html)
 
如果你并不具有以上基础，也不需担心，我将在教程作简单的说明，毕竟我们需要的只是对以上知识的简单了解，而不是掌握。

## 安装我们需要的库
在这里我们使用python自带的pip操作来安装这些库

它们分别是 beautifulsoup4 lxml Django leancloud

打开终端输入

```
pip install *       #  *就是我前面提到的库名
```

如果安装上遇到了问题请自行百度或google

## 项目介绍
这是一个很小型的项目，我们要做的主要分为三个部分 :

* 爬取数据 
* 存储数据
* 页面展示

关于html解析，原博主是使用的是正则表达式，而我使用的是Beautifulsoup，你可以自行选择你喜欢的方式来解析

数据存储使用的是leancloud 当然你也可以使用你喜欢的数据存储方式来完成这个项目

## 爬取网页并解析网页

### 爬虫的编写

我们需要做的第一步就是获取目标网页的**HTML**代码，这里我使用的是python自带的**urllib**库，当然你可以选择更强大的**requests**。

```(python)
from urllib.request import urlopen
#这里我们以斗鱼为例
url = 'https://www.douyu.com/directory/game/LOL'
html = urlopen(url).read().decode('utf-8')  #使用utf-8使得中文可以正常显示
```

完成以上代码后你可以打印html
如果遇到ssl相关的报错可以加上以下代码

```(python)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

html的大概内容如下

```(html)
  <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <title>英雄联盟_英雄联盟直播_网游竞技视频解说攻略_斗鱼 - 每个人的直播平台</title>
                <meta name="renderer" content="webkit|ie-comp|ie-stand">
        <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
                    <meta name="keywords" content="英雄联盟,英雄联盟直播,英雄联盟直播间,英雄联盟直播地址,网游竞技直播,英雄联盟视频解说攻略,热门游戏直播,高清游戏直播,电子竞技直播,手机游戏直播,移动游戏直播" />
                            <meta name="description" content="斗鱼直播拥有海量的英雄联盟直播内容,各类热门英雄联盟精彩赛事直播和各种名家大神直播全天候不间断,英雄联盟大神主播各种操作秀翻天,一起嗨翻全场,全新英雄联盟直播尽在斗鱼直播。" />
                <link href="/favicon.ico" type="image/x-icon" rel=icon>
        <link href="/favicon.ico" type="image/x-icon" rel="shortcut icon">

        <link rel="dns-prefetch" href="//shark.douyucdn.cn">
<link rel="dns-prefetch" href="//apic.douyucdn.cn">
<link rel="dns-prefetch" href="//rpic.douyucdn.cn">
<link rel="dns-prefetch" href="//staticlive.douyucdn.cn">
<link rel="dns-prefetch" href="//webconf.douyucdn.cn">
<link rel="dns-prefetch" href="//res.douyucdn.cn">        <script type="text/javascript" charset="utf-8" src="https://shark.douyucdn.cn/app/douyu/js/com/tinyun.js?nv=v7.720"></script>        
......
</html>
```

打开斗鱼右键审查你同样可以看到类似的代码，实际上这是一个网页的基本结构。有兴趣你可以仔细研究。

### 解析HTML

在这里我使用了**Beautifulsoup**这个简单易用的库

在前面的文件中添加如下代码

```(python)
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, features='lxml') #这里我们使用lxml解析
```

#### 获取主播的ID列表

我们注意到斗鱼的源代码中主播的直播间预览标签都是一样的，它们都长这样

```(html)
<a class="play-list-link"
                    data-rid='1065655'
                    data-tid='1'
                    data-sid='168'
                    data-rpos="0"
                    
                    data-sub_rt="0" href="/1065655" title="哇~这里有个超帅的小姐姐"   target="_blank"                     data-bid='0'>

                <span class="imgbox">
                    <span class="imgbox-corner-mark">
                                                                    </span>
                    <b></b>
                    <i class="black"></i>
                                            <i class="icon_lottery"></i>
                    
                    <img alt="脾气不好天仙老婆的直播" data-original="https://rpic.douyucdn.cn/amrpic-180412/1065655_1750.jpg" src="https://shark.douyucdn.cn/app/douyu/res/page/list-item-def-thumb.gif" width="283" height="163" class="JS_listthumb">
                                    </span>

                <div class="mes">
                    <div class="mes-tit">
                        <h3 class="ellipsis">
                                                        哇~这里有个超帅的小姐姐                        </h3>
                        <span class="tag ellipsis">英雄联盟</span>
                    </div>
                    <p>

                        <span class="dy-name ellipsis fl">脾气不好天仙老婆</span>
                                                <span class="dy-num fr"  >2万</span>
                                            </p>
                </div>


                                    <div class="impress-tag-list">
                                                                                    <span class="impress-tag-item" target="_blank"
                                      data-url="https://www.douyu.com/directory/tags/17538">网瘾少妇</span>
                                                            <span class="impress-tag-item" target="_blank"
                                      data-url="https://www.douyu.com/directory/tags/8027">美的一匹</span>
		......
		
</a>                                
```

先不管内容，把我们要的提取出来

```(python)
play_list = soup.find_all('a', {'class': 'play-list-link'})
#类似还有图片和人数
img_list = soup.find_all('img', {'width': '283', 'height': '163'})
people_list = soup.find_all('span', class_={'dy-num fr'})
play_name = soup.find_all('span', class_={'dy-name ellipsis fl'})
```

可以看到我都是根据相关标签的共同属性来解析的，以上每个变量都是一个数组，它们包含了我们需要的所有信息，数组每个元素都是一个**HTML标签**

做完这些，我们需要对标签的信息进行再提取，我们需要的内容有：

* 主播的ID
* 预览图片的src
* 房间url地址
* 房间标题
* 房间在线人数

在提取这些信息之前，我们先了解一下**leancloud**的基本原理，以方便提取出来就可以进行数据存储

## LeanCloud
### 注册
先上[leancloud官网](https://leancloud.cn/)注册一个账号先，
登陆后访问控制台，打开设置找到自己的应用KEY
你需要的是App ID和App Key

在使用leancloud前，先初始化

```(python)
import leancloud
leancloud.init(APPID, APPKEY)
#这里的APPID, APPKEY是你自己的
```

然后我们就可以用官方给的接口来存数据了

```(python)
Host = leancloud.Object.extend('Host')
host = Host()
host.set(name, data)
```

OK, 我们来存入我们的数据，这里我们定义一个完整的类

```(python)
import re

class Fetcher():
    Host = leancloud.Object.extend('Host')

    def __init__(self):
        self.hosts = []
    #暂时只添加了斗鱼
    def fetch_douyu(self):
        url = 'https://www.douyu.com/directory/game/LOL'
        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, features='lxml')

        play_list = soup.find_all('a', {'class': 'play-list-link'})
        img_list = soup.find_all('img', {'width': '283', 'height': '163'})
        people_list = soup.find_all('span', class_={'dy-num fr'})
        play_name = soup.find_all('span', class_={'dy-name ellipsis fl'})
        for i in range(len(play_list)):
            host = self.Host()
            text = people_list[i].get_text()
            if '万' in text:
                people = int(round(float(re.sub(r'万', '', text)) * 10000))
            else:
                people = int(round(float(text)))
            host.set('type', 'douyu')
            #储存直播间人数
            host.set('num', people)
            #储存主播的名字
            host.set('name', play_name[i].get_text())
            #储存标题
            host.set('title', play_list[i]['title'])
            #直播间地址
            host.set('href', 'https://www.douyu.com' + play_list[i]['href'])
            #直播间图片数据源
            host.set('src', img_list[i]['data-original'])
            self.hosts.append(host)
          
if __name__ == '__main__':
	fetcher = Fetcher()

	fetcher.fetch_douyu()
```

我们运行之后，打开leancloud，就会发现数据已经全部存储进去了

## Django基本用法


安装好Django之后，我们可以直接使用命令行创建一个工程

```
$ django-admin.py startproject LOL  #这里的LOL是项目目录名称
```

再进入我们的工程目录

```
cd LOL
```

可以看到我们的目录内容如下

```
  |--lol
  |manage.py
  |db.sqlite3
```

启动服务

```
$ python manage.py runserver
```
根据弹出信息可知我们的网站运行在了
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

现在我们可以添加webapp项目了，这是我们的网站具体对外提供服务的项目

```
$ python manage.py startapp lolba
```
现在我们的工程目录如下

```
  |--lol
  |--lolba
  |manage.py
  |db.sqlite3
```

进入lol目录，在settings.py中注册我们的app

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   +'lolba'
] 	# +是添加的内容 

#修改语言和时区
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

### 配置url
我们在**lol/urls.py**中添加如下代码

```(python)
urlpatterns = [
    path('admin/', admin.site.urls),
   +path('', include('lolba.urls'))
]
```
这样我们就可以用lolba内部的urls.py文件处理url请求了

创建文件lolba/urls.py, 修改内容如下

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.res_index)
]
```
这意味着我们用views.py中的res_index()函数处理根目录的url请求
不过我们还没写这个函数

打开views.py 我们所有代码如下

```(python)
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from . import clim
import leancloud

# Create your views here.
#页面渲染控制
def res_index(req):
    leancloud.init(clim.APPID, clim.APPKEY)
    Host = leancloud.Object.extend('Host')
    #query = leancloud.Query('Host')
    query = Host.query
    query.select('type', 'num', 'name', 'title', 'href', 'src')
    #按人数降序排列
    query.add_descending('num')
    host_list = query.find()

    hosts = []

    for host in host_list:
        host_info = {}
        host_info['type'] = host.get('type')
        host_info['num'] = host.get('num')
        host_info['name'] = host.get('name')
        host_info['title'] = host.get('title')
        host_info['href'] = host.get('href')
        host_info['src'] = host.get('src')
        hosts.append(host_info)

    return render_to_response('index.html', locals())

#重定义刷新
def fetch(req):
    leancloud.init(clim.APPID, clim.APPKEY)
    query = leancloud.Query('Host')
    DataC = False
    batch = 0
    limit = 1000
    while not DataC:
        query.limit(limit)
        query.skip(batch * limit)
        query.add_descending('createAt')
        resultList = query.find() 
        if len(resultList) < limit:
            DataC = True
            leancloud.Object.destroy_all(resultList)
        batch += 1

    fetcher = clim.Fetcher()
    fetcher.fetch_douyu()

    for host in fetcher.hosts:
        host.save()

    return redirect('/')
```

这其中的要点为：

* 我们定义我们之前提到的res_index()函数
* 我们使用leancloud的API来取出我们存储的数据
* 我们把所有的局部变量传入index.html文件并将其返回给浏览器

没错！我们展示页面的文件就是这个HTML文件，接下来我们完成最后一步

## 页面展示
创建文件lolba/templates/index.html

```(html)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>LOL</title>
</head>
<body>
    {% for host in hosts %}
        <a href="{{ host.href }}">
            <div>
                <div>
                    <img src="{{ host.src }}">
                </div>
                <div>
                    <div>{{ host.title }}</div>
                    <div>{{ host.name }}</div>
                </div>
                <div>
                    <span></span>
                </div>
                <div>
                    <div>{{ host.num }}人</div>
                </div>
            </div>
        </a>
    {% endfor %}
</body>
</html>
```

