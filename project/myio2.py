

def write(filename,mode,buffer):
    with open(filename,mode) as file:
        buffer = buffer + '\n'
        file.writelines(buffer)



def read(filename):
    try:
        with open(filename) as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("the file ",filename," does not exist")


if __name__ == '__main__':
    filename ="c:\\hello12.txt"
    mode ="a"
    buffer = ''' hello,java
             i'am python ,
             where are you\n'
             o,i'am c language'''
    read(filename)
    write(filename,mode,buffer)
    read(filename)
