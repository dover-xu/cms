#!/usr/bin/env python
import requests


def tuisong():
    url = "http://data.zz.baidu.com/urls?site=www.hahajh.com&token=blA9ctURTpFGiMGB"
    filecontents = {'file': open('urls.txt', 'rb')}  # urls.txt为需要推送的URL文件，每行一个
    r = requests.post(url, files=filecontents)
    baiduresult = "推送成功，结果为%s \n" % r.text
    return baiduresult


if __name__ == "__main__":
    ts = tuisong()
    print(ts)
