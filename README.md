# http-server
Implemented with reference to RFC 2616 using Python3

# Usage
On terminal after getting to the directory

To start the server : "bash start.sh <port_number>"

To stop the server : "bash stop.sh"

# Details
Methods implemented : GET, HEAD, POST, PUT, DELETE

Status codes returned on call to any of the method depend on state of the server

Status Codes : 200, 201, 204, 206, 304, 400, 403, 404, 405, 406, 412, 413, 414, 415, 416, 500, 501, 505

# Basic Idea
while(True){

Parse the request obtained;

Check for method to be used:

if (method allowed) and (http-version supported) :

  proceed:
  
  check for headers present in the request
  
  provide required headers in reponse
  
  with suitable status code
  
  if connection requested is persistent then:
  
   continue
   
   else:
   
    connection close
  
  else:
  
   some status code

Taken care of all conditions like forbidden where users are unauthorised, file not found, if partially modified then send that amount of data(Range header), etc 

# Reference

RFC, GFG
