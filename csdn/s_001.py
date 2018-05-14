#p_003.py 
# function:  A spider for all links of CSDN. Getting all article title and created time 
# create by :苏杭
# util pakage: request 
from bs4 import BeautifulSoup
import re
import requests

__name__ == '__main__'


def getHTMLText(url):
    try:  
        r = requests.get(url, timeout=30)  
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
    startURL = 'https://www.csdn.net'
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
        print("title : ", title[0], "time : ", time[0], "link : ", link)



def main():
    spider()


if __name__ == '__main__':
    main()
