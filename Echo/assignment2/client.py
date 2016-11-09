import socket, pickle, sys
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = ('localhost' , 8080)
print>>sys.stderr, 'connecting to %s port %s...' % server_ip
client.connect(server_ip)
try:
	print >>sys.stderr, 'Please enter your name: (then press enter)'
	name = sys.stdin.readline()
	print >>sys.stderr, 'Please enter your age: (then press enter)'
	age = sys.stdin.readline()
	print >>sys.stderr, 'Please enter your nummer: (then press enter)'
	numb = sys.stdin.readline()
	data = ([name, age, numb])
	data_to_string = pickle.dumps(data)
	client.sendall(data_to_string)
	print >>sys.stderr, 'closing socket...'
finally:
	client.close()