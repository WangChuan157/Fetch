import leancloud
from clim import APPID, APPKEY

leancloud.init(APPID, APPKEY)
Host = leancloud.Object.extend('Host')
#query = leancloud.Query('Host')
query = Host.query
query.select('type', 'num', 'name', 'title', 'href', 'src')
#按人数降序排列
query.add_ascending('num')
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

print (len(hosts))
for host in hosts:
    print(host['name'])

    