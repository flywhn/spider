import threading
import queue
import spider
import htmlparser
import tools
import time
import comment

qplace = queue.Queue() #place of url 队列。
qsight = queue.Queue() #sight of url 队列
setplace = set() #存放place of url的md5值的bytes，防止重复采集url
setsight = set() #存放sight of url

mutexOfplace = threading._allocate_lock()#分配一个线程锁
mutexOfsight = threading._allocate_lock()#分配一个线程锁


resource = 'http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView'

def worksight():
    if qsight.empty() == True:
        time.sleep(5)
    while qsight.empty() != True:
        url = tools.work(qsight,setsight,mutexOfsight)
        if url :
            if url.startswith("http://you.ctrip.com"):
                pass
            else:
                url = 'http://you.ctrip.com' + url
            html_code = spider.request_html(url)
            time.sleep(1)
            if html_code :
                print(url)
                hp = htmlparser.MyParser3(url)
                hp.feed(html_code)
                print(hp.title, hp.poiID, hp.page)
                if len(hp.poiID) == 0  or hp.poiID.strip().isnumeric() != True:
                    print("failed")
                    continue
                comm = comment.Comment(hp)

                hp.close()

                hp2 = htmlparser.MyParser2()
                id=1
                try:
                    while comm.data['pagenow']<comm.page:
                        comm.data['pagenow']+=1
                        if comm.data['pagenow']%100 == 0:
                            time.sleep(2)
                        response=spider.request_ajax_url(resource,body=comm.data,referer=url)

                        hp2.feed(response)
                        for item in hp2.item:
                            comm.text += '<p id='+str(id)+'>'+str(item)+'</p>\n\n'
                            id+=1
                        hp2.text = ''
                        hp2.item = []


                except Exception as e:
                    print(e)
                comm.text = "<div>\n"+comm.text+"</div>"
                comm.save()

                hp2.close()






def work(qlist,sett,lockk,qdes,special):

     url = tools.work(qlist,sett,lockk)
     if url :

         if url.startswith("http://you.ctrip.com"):
             pass
         else :
             url = 'http://you.ctrip.com'+url
         html_code = spider.request_html(url)


         if html_code:
             print(url)
             hp = htmlparser.MyParser(special)
             hp.feed(html_code)
             for link in hp.links:
                 qdes.put(link)

             hp.close()



def run():
    while qplace.empty()!=True:
        work(qplace,setplace,mutexOfplace,qsight,'/sight/')











if __name__ == "__main__":

    qsight.put("/sight/madrid378/12674.html")
    qsight.put("http://you.ctrip.com/sight/phuket364/18402.html")
    qsight.put("http://you.ctrip.com/sight/shenzhen26/50545.html")
    qsight.put("http://you.ctrip.com/sight/tulufan35/4674.html")
    qsight.put("http://you.ctrip.com/sight/hongkong38/22943.html")


    try:
        qplace.put("/place/")
        work(qplace,setplace,mutexOfplace,qplace,'/place/')




        threadPool = []
        for i in range(4):
            threadPool.append(threading.Thread(target=run))



        for i in range(6):
            threadPool.append(threading.Thread(target=worksight))
        for th in threadPool:
            th.start()
            th.join()

    except Exception as e:
        print(e)
    print('done')























    #关闭打开的资源。












