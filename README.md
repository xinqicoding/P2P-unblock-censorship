# P2P-unblock-censorship

### The idea of this program is to free the Internet. It is a P2P tool to unblock the network censorship set by certain governments.  

##### Instructions on how to run the code
- Configure the proxy setting in browser. We recommend using firefox. In the setting -> advance -> network set the proxy configuration to "Manual configuration". Set the HTTP proxy to localhost and port to the port you like. (Do not use the system reserved port)

- Run the server.py under root priviledge. (By default, server will save the http responses in the Proxy/server_data/request_count#/proxy_data#)

- Run the client.py under root prigiledge with the command python client.py <portnumber>. (By default, server will save the http request in the Proxy/client_data/request#)
