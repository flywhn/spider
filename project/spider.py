# -*- coding: utf-8 -*-
from urllib import request
from urllib import parse
import htmlparser
headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Connection':'keep-alive'
}
def request_ajax_url(url,body,referer=None,cookie=None,**headers):
    req = request.Request(url)
    postBody = parse.urlencode(body)

    req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0')
    req.add_header('Content-Length',str(len(postBody)))
    req.add_header('Connection','keep-alive')
    if referer:
        req.add_header('Referer',referer)
    try:
        response = request.urlopen(req,postBody.encode('UTF-8'))
        if response:
            return response.read().decode(encoding='utf-8',errors='replace')
    except Exception as e:
        print(str(e))



def request_html(url):
    req = request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0')
    try:
        res = request.urlopen(req)
        htmlText = res.read()
        return htmlText.decode(encoding='utf-8',errors='replace')
    except Exception as e:
        print(str(e))


if __name__=='__main__':

    data = {}
    data['poiID']=78738
    data['pagenow']=18
    '''
    data['districtId']='378'
    data['districtEname']='Madrid'
    data['order']='3.0'
    data['star']='0.0'
    data['tourist']='0.0'
    data['resourceId']='12674'
    data['resourcetype']='2'
    '''



    url='http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView'
    referer = "http://you.ctrip.com/sight/madrid378/12674.html"
    response = request_ajax_url(url,data)
    html_code = request_html(referer)
    hp=htmlparser.MyParser3(url)
    #print(html_code)


    hp.feed(html_code)
    print(hp.poiID,hp.page,hp.title,hp.description)








