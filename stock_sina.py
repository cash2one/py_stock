#:coding:utf8
import requests
import datetime
import time
import os
from bs4 import BeautifulSoup
doc='''
http://itindex.net/detail/49971-sina-%E8%82%A1%E7%A5%A8-%E6%95%B0%E6%8D%AE
查看日K线图：
http://image.sinajs.cn/newchart/daily/n/sh601006.gif
分时线的查询：
http://image.sinajs.cn/newchart/min/n/sh000001.gif
日K线查询：
http://image.sinajs.cn/newchart/daily/n/sh000001.gif
周K线查询：
http://image.sinajs.cn/newchart/weekly/n/sh000001.gif
月K线查询：
http://image.sinajs.cn/newchart/monthly/n/sh000001.gif
http://hq.sinajs.cn/list=sh601006
http://itindex.net/detail/54764-%E8%82%A1%E7%A5%A8-%E5%AE%9E%E6%97%B6-%E4%BA%A4%E6%98%93
'''
from cStringIO import StringIO
lst = '''
s_sz399001
s_sh000300
# s_sz150028
# s_sz399415
# s_sh603333
# s_sh000001
# s_sz399006
# s_sz300431
# s_sz002702
# s_sz000025
# s_sh600401
# s_sh600962
# s_sh601001
# s_sh600650
# s_sz300330
# s_sz300072
# s_sz000629
s_sh603077
s_sz002702
'''


def u2g(st): return st.encode('gbk','ignore')


def parse_js(st):
    rs = []
    st = st.replace('var hq_str_s_', '').replace(
        '=\"', '\t').replace('\";', '').replace(',', '\t')
    for l in StringIO(st):
        row=l.strip().split('\t')[0:]
        row[0]=row[0][:]
        rs.append(row)
    return rs

# print int(datetime.datetime.ctime(now))


def ts_to_str(i):
    return datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')


def get_index(lst):
    lst = ','.join([s.strip() for s in StringIO(lst) if not s.startswith('#')])
    tobj = time.time()
    gt = '%d' % (tobj * 1000)
    print ts_to_str(tobj)  # 1435729332785
    url = 'http://hq.sinajs.cn/rn=%s&list=s_%s' % (gt, lst)
    print url
    res = requests.get(url)
    rs = parse_js(u2g(res.text))
    for row in rs:
        print ''.join(map(lambda x: '%10s' % x, row))
        
def guba(code):
    import urllib
    site='http://guba.eastmoney.com'
    url='%s/list,%s.html'%(site,code)
    # url='stockpage.10jqka.com.cn/%s'%code
    print url
    html=urllib.urlopen(url).read()
    # print html
    soup=BeautifulSoup(html)
    for tag in soup.findAll('span',class_='l3')[6:16]:
        print u2g(tag.text ),'|',
        atag=tag.findAll('a')
        if len(atag)>0:
            print site+"/"+atag[0]['href']
        # print tag ,
    print ''
    
def main():
    for i in range(1):
        get_index(lst)
        time.sleep(2)
        os.system('cls')

if __name__=='__main__':
    main()
    # guba('600401')
    # guba('600962')
    # guba('300072')