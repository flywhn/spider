import config

def write(filename,mode,buffer):
    path = config.data
    filename = path+filename
    file = open(filename,mode,encoding='utf-8')
    try:
        buffer = buffer + '\n'
        file.write(buffer)
        
        print("The file has been append")
    except IOError:
        print("The file can not write,Please check!")
        exit()
    finally:
        file.close()


def read(filename):
    try:
        file = open(filename)
    except FileNotFoundError:
        print("the file ",filename," does not exist")
        exit(-1)
    try: 
        content = file.read()
        print(content)
    except IOError:
        print("The file can not read,Please check!")
    finally:
        file.close()


def work(qlist,sett,lock):

    while qlist.empty()!=True:
        element = qlist.get()
        lock.acquire()
        if sett.__contains__(element):
            lock.release()
            continue
        else:
            sett.add(element)
            lock.release()
            return element

if __name__ == '__main__':
    filename ="c:\\hello12.txt"
    mode ="a"
    buffer = ''' hello,java
             i'am python ,
             where are you'
             o,i'am c language'''
    #write(filename,mode,buffer)
    read(filename)
