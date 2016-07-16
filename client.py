import os,sys,thread,socket,shutil

# This part of program is used to establish connection with client app (ie. browser)
# the application accepts the browser http request and put that into files and share with server application
# the application also detect and parse new http response files into real http response and pipe back to browser


# Client request located in the directory Proxy/client_data/request#
# Server reply located in the directory Proxy/server_data/request_count#/proxy_data#
# request# is the ith request, and request_count# is the ith request_count, and proxy_data# is the ith proxy_data

#***********Constant****************** 
MAX_BUFFER_SIZE = 4096				# The buffer size to receive once
BACKLOG = 50						# Number of pending connections 


# Main
def main():

	# check the length of command running
	if (len(sys.argv) < 2):
		print "usage: proxy <port>"
		return sys.stdout
	# host and port info.
	host = ''               # blank for localhost
	port = int(sys.argv[1]) # port from argument
	print "Starting client at port " + str(port)
	try:
		# create a socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# associate the socket to host and port
		s.bind((host, port))

		# listenning
		s.listen(BACKLOG)

	except socket.error, (value, message):
		if s:
			s.close()
		print "Could not open socket:", message
		sys.exit(1)

	request_count = 0
	# get the connection from client
	while 1:
		conn, client_addr = s.accept()
		# create a thread to handle request
		thread.start_new_thread(client_thread, (conn, client_addr, request_count))
		request_count += 1


def client_thread(conn, client_addr, request_count):

	# get the request from browser
	request = conn.recv(MAX_BUFFER_SIZE)

	# write the request into file 
	filename = "Proxy/client_data/request"+str(request_count)
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, "w") as f:
		f.write(request)
		f.close()

	try:
		reply_count = 0
		while 1:
			# check if new reply data has arrived in folder, if so, parse and send to browser
			filename = "Proxy/server_data/" + str(request_count) + "/proxy_data" + str(reply_count)
			if os.path.exists(filename):
				print "Found new http reply for request " + str(request_count)
				f = open(filename)
				newData = f.read()
				f.close()
				if (len(newData) > 0):
					conn.send(newData)
					reply_count += 1
					print "send browser data"
				else:
					break
		print "closing thread"
		conn.close()
	except socket.error, (value, message):
		if conn:
			conn.close()
		print "Runtime Error:", message
		sys.exit(1)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "Ctrl C - Stopping server"
		shutil.rmtree('Proxy')
		sys.exit(1)
