'''
Get Page using GET method
Default  using HTTP Protocol
'''
import socket
import config
import statistics
import datetime
import myio2
from urllib import parse


socket.setdefaulttimeout(config.timeout)

class Error404(Exception):
    ''' Can not fing the page.'''
    pass

class ErrorOther(Exception):
    '''Some other exception'''
    def __init__(self,code):
        self.code = code
        pass



def downPage(hostname ,filename ,log=None):
    if not log:
        log = open(config.log,"a+")
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if config.DNSCache.__contains__(hostname):
            addr = config.DNSCache[hostname]
        else:
            addr = socket.gethostbyname(hostname)
            config.DNSCache[hostname]=addr
        #connect to http server ,default port 80
        s.connect((addr,80))
        data = {}
        data['poiID']="78738"
        data['districtId']='378'
        data['districtEname']='Madrid'
        data['pagenow']=2
        data['order']='3.0'
        data['star']='0.0'
        data['tourist']='0.0'
        data['resourceId']='12674'
        data['resourcetype']='2'

        print(dir(parse))
        msg  = 'POST '+filename+' HTTP/1.1\r\n'
        msg += 'Host: '+hostname+'\r\n'
        msg += 'Content-Type: application/x-www-form-urlencoded\r\n'
        msg += 'Content-Length: '+str(len(data))+'\r\n\r\n'
        msg += parse.urlencode(data)

        # msg  = 'GET '+filename+' HTTP/1.0\r\n'
        #msg += 'Host: '+hostname+'\r\n'
        #msg += 'User-Agent:Admin\r\n\r\n'
        content = ''

        s.sendall(msg.encode())

        first = True
        while True:

            msg = s.recv(40960)

            msg = msg.decode(errors='ignore')
            if len(msg):
                content +=msg
            else:

                break
            #Head information must be in the first recv buffer
            if first:
                first = False
                print("msg is",msg,"end of msg")
                headpos = msg.index("\r\n\r\n")
                print('headpos',headpos)
                code = dealwithHead(msg[:headpos])
                print('code',code)
                if code == '200':
                    pass
                elif code == '404':
                    raise Error404
                else :
                    raise ErrorOther(code)

        s.shutdown(socket.SHUT_RDWR)
        s.close()
        log.write(hostname+' '+filename+"\t\tSucceed\t\t"+str(datetime.datetime.now())+'\n')
        return content
    except Error404 :
        log.write(hostname+' '+filename+"\t\tError404 not found\t\t"+str(datetime.datetime.now())+'\n')
        statistics.failed_url +=1
        return None
    except ErrorOther as e:
        log.write(hostname+' '+filename+'\t\t'+e.code+'\t\t'+str(datetime.datetime.now())+'\n')
        statistics.other_url +=1
        return None
    except socket.timeout:
        log.write(hostname+' '+filename+"\t\tTimeOut\t\t"+str(datetime.datetime.now())+'\n')
        statistics.timeout_url +=1
        return None
    except Exception as e:
        log.write(hostname+' '+filename+'\t\t'+str(e)+'\t\t'+str(datetime.datetime.now())+'\n')
        statistics.other_url +=1
        return None

def dealwithHead(head):
    '''deal with HTTP HEAD'''
    lines = head.splitlines()
    fstline = lines[0]
    code = fstline.split()[1]
    return code



def parseURL(url):
    '''Parse a url to hostname+filename'''
    try:
        u = url.strip().strip('\n').strip('\r').strip('\t')
        if u.startswith('http://'):
            u = u[7:]
        else :
            return None,None
        if u.find('/')>0:
            p = u.index('/')
        else :
            return None,None

        hostname = u[:p]
        filename = u[p:]

        return hostname, filename
    except Exception as e:
        print("Parse wrong: ",url,e)





def writeDnsCache():
    '''print DNS cache'''
    n = 1
    for hostname in config.DNSCache.keys():
        print(n,'\t',hostname,'\t',config.DNSCache.get(hostname))
        n += 1



def test(url):
    hostname, filename = parseURL(url)
    print(hostname+' ## '+filename)
    print(downPage(hostname=hostname,filename=filename,log=None))


if __name__ == '__main__':
    urlSet = (
        "http://you.ctrip.com/sight/madrid378/12674.html",
    )

    for url in urlSet:
        test(url)

    writeDnsCache()







