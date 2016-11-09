import pickle, socket, sys, string
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)
try:
	#print >>sys.stderr, 'waiting for a connection...'
	connection, address = server.accept()
	#print >>sys.stderr, 'connection from', address
	while True:
		buf = connection.recv(1024)
		data = pickle.loads(buf)
		if len(data) > 0:
			print 'Name: {0};'.format(data[0].strip()), '\nAge: {0};'.format(data[1].strip()), '\nMatrikelnummer: {0}'.format(data[2].strip())
			break
	#print >>sys.stderr, 'closing the socket'
finally:
	server.close()