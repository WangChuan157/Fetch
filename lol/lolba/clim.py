from urllib.request import urlopen
import ssl
import re
from bs4 import BeautifulSoup
import leancloud
ssl._create_default_https_context = ssl._create_unverified_context

APPID = '69Bvdi66JanILWrRaYMp9EcR-gzGzoHsz'
APPKEY = 'c1nLqIurkdP2mKMtBAROvGwx'
leancloud.init(APPID, APPKEY)

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