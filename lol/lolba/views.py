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