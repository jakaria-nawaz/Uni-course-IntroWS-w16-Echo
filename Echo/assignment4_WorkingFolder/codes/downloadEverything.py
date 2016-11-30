import re
from urlparse import urljoin
from urlparse import urlparse
from client import receive_respone
srcs = []

file1 = 'index.php'
ur = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
def download_everything(file_name, url):
    with open(file_name, 'rb+') as f:
        data = f.readlines()
    for dat in data:
        if re.search('<img ', dat):
            for x in re.findall('src="(.*?)"', dat, re.DOTALL):
                srcs.append(urljoin(url, x))
    return srcs

urls = download_everything(file1, ur)
for url1 in urls:
    print url1
    parse = urlparse(url1)
    receive_respone(url1)
