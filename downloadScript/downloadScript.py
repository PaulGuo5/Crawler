import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup


def get_content(url, search_content):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    data={
    'geneSetName': search_content,
    'Search': 'Search'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout,params = data)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def get_url(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    data = body.find('table', {'class': 'lists2'})
    tr = data.find('tr')
    td = tr.find_all('td')
    for col in td:
        content_tag = col.find_all('a')
        for content in content_tag:
            final.append(content['href'])
    return final

def get_download_url(urls):
    key_words = []
    for url in urls:
        key_words.append("http://software.broadinstitute.org/gsea/msigdb/download_geneset.jsp?geneSetName="+url[6:-5]+"&fileType=grp")
    return key_words


if __name__ == '__main__':
    url ='http://software.broadinstitute.org/gsea/msigdb/genesets.jsp'
    html = get_content(url,"metabolism")
    # print(html)
    new_url = get_url(html)
    # print(result)
    result = get_download_url(new_url)
    print(result)

