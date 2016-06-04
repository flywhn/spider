import tools
class Comment(object):
    def __init__(self,hp):
        self.title =hp.title
        self.page = int(hp.page)
        self.poiid = int(hp.poiID)
        self.description = '<h1>'+hp.description.strip()+'</h1>\n\n'
        self.text=''
        self.data = {"poiID":self.poiid, "pagenow":0}



    #self.url[:-5].replace('/','%')
    def save(self):
        if self.title:
            tools.write(self.title+'.txt',mode='w',buffer='<title>'+self.title+'</title>\n\n'+self.description+self.text)




if __name__ == '__main__':
    pass


