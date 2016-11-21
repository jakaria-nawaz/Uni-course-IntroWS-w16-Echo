import socket
from urlparse import urlparse
import os

# url = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
url = 'http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg'


def separate_header(content):
    header = content.split("\r\n\r\n")[0]
    with open('index.php.header', 'wb+') as f:
        f.write(header)
    return header


def receive_respone(path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parsedurl = urlparse(path)
    server_ip = (socket.gethostbyname(parsedurl.netloc), 80)
    sock.connect(server_ip)
    CRLF = '\r\n\r\n'

    sock.send("GET {0} HTTP/1.0{1}".format(parsedurl.path, CRLF))

    first_data = sock.recv(100)
    if first_data.find('OK') != -1:

        def recvall(sock1):
            data = ""
            part = None
            while part != "":
                part = sock1.recv(100000)
                data += part
            return data

        all_content = first_data + recvall(sock)
        hdr = separate_header(all_content)
        # print hdr
        if hdr.find('image') != -1:
            with open(os.path.basename(parsedurl.path), 'wb+') as f:
                f.write(all_content.split("\r\n\r\n")[1])
        else:
            with open('index.php', 'wb+') as f:
                f.write(all_content)

        return all_content
    else:
        print 'status is not OK'


receive_respone(url)





