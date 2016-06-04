from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self,special):
        HTMLParser.__init__(self)
        self.special = special
        self.links = []




    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for(var,value) in attrs :
                if var == "href":
                    if value.__contains__(self.special):

                        self.links.append(value)








class MyParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=False
        self.text=''
        self.item=[]

    def handle_starttag(self,tag,attrs):
        if tag=='span':
            for(var,value) in attrs:
                if var =='class' and value =='heightbox':
                    self.flag=True

    def handle_endtag(self, tag):
        if tag=='span':
            self.flag=False
            if self.text:
                self.item.append(self.text)
                self.text=''

    def handle_data(self, data):
        if self.flag == True:
            self.text+=data


class MyParser3(HTMLParser):
    def __init__(self,url):
        HTMLParser.__init__(self)
        self.url = url
        self.title =''
        self.flag=False
        self.nextdiv=False
        self.nextp=False
        self.findpage= False
        self.finddesc = False
        self.findtitle = False
        self.poiID=''
        self.page=''
        self.description= ''




    def handle_starttag(self,tag,attrs):
        if self.flag==False and tag=='a':
            for(var,value) in attrs:
                if var =='id' and value =='jieshao':
                    self.flag=True

        if tag=='b':
            for(var,value) in attrs:
                if var =='class' and value =='numpage':
                    self.findpage=True
        if self.nextdiv==False and self.flag==True and tag=='div':
            for(var,value) in attrs:
                if var=='class' and value =='toggle_l':

                    self.nextdiv=True;

        if self.nextp==False and self.nextdiv==True and tag=='p':
            self.nextp=True

        if len(self.title)==0 and tag =='h1':
            self.findtitle = True








        if tag=='a':
            for(var,value) in attrs:
                if var =='href' and value.__contains__("/dianping/edit/"):
                     self.poiID=value[15:-5]

    def handle_endtag(self, tag):
        if self.nextp ==True and tag=='div':
            self.finddesc=True

    def handle_data(self, data):
        if  self.nextp==True  and self.finddesc==False:
            self.description+=data
        if  self.findpage == True and len(self.page)==0:
            self.page = data
        if  self.findtitle == True and len(self.title)==0:
            self.title=data








if __name__ == "__main__":

    html_code = open("F:/project/project.html.txt",'r').read()
    url ='http://you.ctrip.com/sight/madrid378/12674.html'
    hp = MyParser3()

    hp.feed(html_code)

    hp.close()

