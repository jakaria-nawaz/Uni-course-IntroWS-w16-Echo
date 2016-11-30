import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8081))
server.listen(5)
try:
    connection, address = server.accept()
    while True:
        buf = connection.recv(1024)
        if len(buf) > 0:
            protocol = buf.split("://", 1)
            y = protocol[1].split("/", 1)
            try:  # if there's no port number, we assumed that it's not common to have it
                domain = y[0].split(":")
                port = domain[1]
                subdomains = domain[0].split(".")
                print 'Domain ', domain[0]
                print 'Port number ', port
            except:
                print 'No port number'
                domain = y[0]
                subdomains = domain.split(".")
                print 'Domain ', domain
            path = y[1].split("?")
            valueFrag = path[1].split("#")
            param = valueFrag[0].split("&")
            print 'Protocol ', protocol[0]
            print 'Sub-Domain ', subdomains
            print 'Path', path[0]
            print 'Parameters ', param
            print 'Fragment ', valueFrag[1]
            break
finally:
    server.close()
