import os,sys,thread,socket,shutil

#  This part of program is used to fetch request files from drive directory,
#  parse the files back to requests and send to the original destination,
#  then get the response from the server, and store back into file


# Client request located in the directory Proxy/client_data/request#
# Server reply located in the directory Proxy/server_data/request_count#/proxy_data#
# request# is the ith request, and request_count# is the ith request_count, and proxy_data# is the ith proxy_data

#***********Constant****************** 
MAX_BUFFER_SIZE = 4096				# The buffer size to receive once
BACKLOG = 50						# Number of pending connections 


 MAIN 
def main():
  print "Starting the server"
  request_count = 0;
  while (1):
    # check if new webserver request in the directory, if so, start a new connection
    filename = "Proxy/client_data/request"+str(request_count)
    if os.path.exists(filename):
      print "Found new http request"
      thread.start_new_thread(server_thread, (request_count,))
      request_count += 1





# The thread for reading the request from file, and start the connection with the original 
# server, and send the response back to the file
def server_thread(request_count):

  # read the request from file
  filename = "Proxy/client_data/request"+str(request_count)
  f = open(filename)
  request = f.read()
  f.close()

  # parse the first line
  first_line = request.split('\n')[0]
  print first_line
  # get the url
  if first_line == "":
    sys.exit(1)
  url = first_line.split(' ')[1]
  # find the webserver and port
  http_pos = url.find("://")          # find pos of ://
  if (http_pos==-1):
    temp = url
  else:
    temp = url[(http_pos+3):]       # get the rest of url

  port_pos = temp.find(":")           # find the port pos (if any)

  # find end of web server
  webserver_pos = temp.find("/")
  if webserver_pos == -1:
    webserver_pos = len(temp)

  # locate the web server
  webserver = ""
  port = -1
  if (port_pos==-1 or webserver_pos < port_pos):      # default port
    port = 80
    webserver = temp[:webserver_pos]
  else:       # specific port
    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
    webserver = temp[:port_pos]

  try:
    # create a socket to connect to the web server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(request)         # send request to webserver
    reply_count = 0
    while 1:
      # receive data from web server
      # s.settimeout(5.0)
      data = s.recv(MAX_BUFFER_SIZE)
      # s.settimeout(None)      		
      filename = "Proxy/server_data/" + str(request_count) + "/proxy_data" + str(reply_count)
      if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
      with open(filename, "w") as f:
        f.write(data)
        f.close()
        #check if end of reply
      if (len(data) > 0):
        reply_count += 1
      else:
        break
    s.close()
  except socket.error, (value, message):
    if s:
      s.close()
    print "Runtime Error:", message
    sys.exit(1)



if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print "Ctrl C - Stopping server"
    shutil.rmtree('Proxy')
    sys.exit(1)
