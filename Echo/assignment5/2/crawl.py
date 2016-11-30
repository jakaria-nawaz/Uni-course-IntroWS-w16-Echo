from urlparse import urlparse
from urlparse import urljoin
from Queue import Queue
from io import open
import socket
import re
import os

server_ip = "http://141.26.208.82/"
prsurl = urlparse(server_ip)
global alreadydownloaded
global paths
global failed
global downloaded
downloaded = []  # local paths of the downloaded files
failed = []
paths = []  # URLs of the downloaded files
alreadydownloaded = []


def recvall(sock1):  # receiving all data
    dat = ""
    part = None
    while part != "":
        part = sock1.recv(2046)
        dat += part
    return dat


def dohttpgetrequest(youarel):  # making request and downloading file
    """

    :rtype: str full path of the file
    """
    try:
        parsed = urlparse(youarel)
        path = parsed.path
    except:
        print 'URL parsing is wrong '
        failed.append(youarel)
        pass
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80
    crlf = "\r\n\r\n"
    client.connect(('141.26.208.82', port))
    try:
        request = "GET {0} HTTP/1.0{1}".format(path, crlf)
        client.send(request.encode())
    except:
        print 'problem in request'
        failed.append(path)
        pass
    data = recvall(client)
    body = data.split("\r\n\r\n")[1]
    if not os.path.exists(os.getcwd() + '/output' + os.path.dirname(path)):
        os.makedirs(os.getcwd() + '/output' + os.path.dirname(path))
    dir1 = os.getcwd() + '/output' + os.path.dirname(path)
    filename1 = dir1 + '/' + os.path.basename(path)
    if os.path.isfile(filename1):
        alreadydownloaded.append(filename1)
    else:
        try:
            filename1 = dir1 + '/' + os.path.basename(path)
            with open(filename1, 'wb+') as f:
                f.write(body)
            downloaded.append(filename1)
            return filename1
        except IOError:
            print 'saving file issue ', youarel
            failed.append(filename1)
            pass


def resolve_url_path(path):  # resolving the dots in the URLs
    """

    :rtype: str
    """
    segments = path.split('/')
    segments = [segment + '/' for segment in segments[:-1]] + [segments[-1]]
    resolved = []
    for segment in segments:
        if segment in ('../', '..'):
            if resolved[1:]:
                resolved.pop()
        elif segment not in ('./', '.'):
            resolved.append(segment)
    return ''.join(resolved)


def readfile(ff):
    fo = open(ff, encoding="utf8")
    fill = fo.read()
    fo.close()
    return fill


def findandsave(base):  # finding the URL links <a tags in a Queue
    """

    :rtype: Queue
    """
    internalurls = Queue()
    if base:
        try:
            fx = readfile(base)
            links = re.findall('<a href=[\'"]?([^\'" >]+)', fx, re.DOTALL)
            for link in links:
                merge = urljoin(server_ip, link)
                check = urlparse(merge).netloc
                if urlparse(merge).path != "/":
                    if check == prsurl.netloc:
                        esm = urljoin(server_ip, resolve_url_path(link))
                        internalurls.put(esm)
        except:
            print 'something went wrong in the saveandfind function: ', base
    return internalurls


def downloadlist(alist):  # downloading the Queues
    blistt = alist
    while not blistt.empty():
        x = blistt.get()
        if x not in paths:
            y = dohttpgetrequest(x)
            paths.append(x)
            z = findandsave(y)
            downloadlist(z)

# downloading germany.html as a first web page
gerpath = "http://141.26.208.82/articles/g/e/r/Germany.html"
if gerpath not in paths:
    filename = dohttpgetrequest("http://141.26.208.82/articles/g/e/r/Germany.html")
    paths.append(gerpath)
thelist = findandsave(filename)
downloadlist(thelist)

# recording data in files, NOTE they're in appending mode
with open('downloaded.txt', 'ab+') as fil:
    for down in downloaded:
        fil.write(down + '\n')
with open('failed.txt', 'ab+') as fil:
    for fail in failed:
        fil.write(fail + '\n')
with open('alreadydownloaded.txt', 'ab+') as fil:
    for already in alreadydownloaded:
        fil.write(already + '\n')
with open('paths.txt', 'ab+') as fil:
    for pth in paths:
        fil.write(pth + '\n')
