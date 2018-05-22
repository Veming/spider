#p_003.py 
# function:  A spider for all links of CSDN. Getting all article title and created time 
# create by :苏杭
# util pakage: request 
# 使用方法： 从端口号为6379的数据库中,使用lpop方法弹出健值为 title 和 time 的列表就可以得到一条数据， title和time必须一起弹出才能对应上，否则会出现失序
# 注意事项： 若从数据库客户端直接读数据的时候若出现乱码 请使用 redis-cli --raw 访问redis客户端
from bs4 import BeautifulSoup
from redis import StrictRedis
import re
import requests

redis = StrictRedis(host='localhost', port=6379, db=0)

__name__ == '__main__'


def getHTMLText(url):
    try:  
        headers = {
            'Host': 'blog.csdn.net',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://blog.csdn.net/nav/cloud',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tingyun-Id': 'wl4EtIR_7Is;r=976669768',
            'Cookie': 'uuid_tt_dd=4099473511411770564_20180522; dc_session_id=10_1526976401745.516297; TY_SESSION_ID=44a0e163-9d87-49c1-8a47-8cb70dbb5695; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1526976641; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1526976651; ADHOC_MEMBERSHIP_CLIENT_ID1.0=80021b53-245d-2f0a-9e86-a5c831756bf7; dc_tos=p94eq2',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        r = requests.get(url, headers = headers, timeout=30)  
        r.raise_for_status()  
        r.encoding = r.apparent_encoding  
        return r.text  
    except:  
        return ""  


def getLinks(html,linkPool):
    urlRule = 'https://blog.csdn.net/\w*/article/details/\d*'    
    soup = BeautifulSoup(html,'html.parser')
    unlinks = soup.find_all('a')
    links = []
    for link in unlinks:
        href = link.attrs.get('href')
        if href == None :
            continue
        else:
            flag = re.search(urlRule, href)
        if linkPool.get(href) == None and flag:
            linkPool[href] = True
            links.append(href)
        else:
            continue
    return links

    

def spider():
    startURL = 'https://www.csdn.net/nav/cloud'
    titleRule = '<h6 class="title-article">(.*?)</h6>'
    timeRule = '<span class="time">(.*?)</span>'

    linkPool = {}
    linkPool[startURL] = True

    links = []
    links.append(startURL)

    for link in links:
        html = getHTMLText(link)
        links.extend(getLinks(html,linkPool))
        title = re.findall(titleRule,html)
        time = re.findall(timeRule,html)
        if len(title) == 0 or len(time) == 0 :
            continue
        data = "title : "+ title[0]+ "time : "+ time[0], "link : "+ link
        # redis.publish("redisChat",data)
        redis.rpush('title',title)
        redis.rpush('time',time)
        print("title : ", title[0], "time : ", time[0], "link : ", link)



def main():
    spider()


if __name__ == '__main__':
    main()



