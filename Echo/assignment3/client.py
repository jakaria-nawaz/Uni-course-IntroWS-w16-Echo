import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = ('localhost', 8081)
print 'connecting to %s port %s...' % server_ip
try:
    client.connect(server_ip)
except socket.error, exc:
    print "Caught exception socket.error : %s" % exc
while True:
    url = raw_input('Please enter a URL that ends with \\r \\n:\n')
    try:
        if url.endswith('\\r \\n'):
            url2 = url.split('\\r \\n')
            client.send(url2[0])
    except:
        print 'Your URL does not end with \\r \\n try again'
        continue
    if url.endswith('\\r \\n'):
        break
client.close()
