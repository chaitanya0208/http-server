from socket import *
import time 
import datetime
import os
import mimetypes
import sys
from threading import Thread
import urllib.parse
from config import *

def header_val(request, header_name):
    if header_name in request:
        header_val = (request[request.index(header_name)+len(header_name)+2:]).split("\r\n")[0]
        return header_val
    return ""

def cont_length(filename):
    file_size = os.path.getsize(filename)
    return str(file_size)


def getEtag(filename):
    file_size = os.path.getsize(filename)
    modified = os.path.getmtime(filename)
    etag = str(modified)+str(file_size)
    return etag
    

def last_modify(filename):
    last_modified = time.ctime(os.path.getmtime(filename)).split(' ')
    for i in last_modified:
        if len(i) == 0:  #if date of type 01, ...
            last_modified.remove(i)
    last_modified[0] += ','
    last_modified[1], last_modified[2] = last_modified[2], last_modified[1]
    last_modified[3], last_modified[4] = last_modified[4], last_modified[3]
    return (' ').join(last_modified) + ' GMT'


def date_time():
    now = datetime.datetime.now()
    today = now.strftime("%a, %d %b %Y ")
    gmt = time.gmtime(time.time())
    today += str(gmt.tm_hour) + ":" + str(gmt.tm_min) +":"+ str(gmt.tm_sec)+" GMT"
    return today

def content_type(filename):
    return mimetypes.guess_type(filename)[0]

def set_cookies():
    for c in cookies:
        if c not in cookies_sent:
            cookie_name = c
            cookie_value = cookies[cookie_name]
            #expiry_date = cookie_date()
            DateTime = (datetime.datetime.now() + datetime.timedelta(days=1))
            expiry_date = DateTime.strftime("%a, %d %B %Y %I:%M:%S ")
            if cookie_name not in cookies_sent.keys():
                cookies_sent[cookie_name] = expiry_date
            break
        else:
            continue
    if cookie_name:
        DateTime = (datetime.datetime.now() + datetime.timedelta(days=1))
        cookie = "Set-Cookie: " + cookie_name + "=" + cookie_value + ";"+ "Expires="
        cookie += DateTime.strftime("%a, %d %B %Y %I:%M:%S")+" GMT;"
        return cookie
    else:
        return None


def statusCode_200(filename):
    status_line = "HTTP/1.1 "+ "200 OK" + "\r\n"
    response_headers = "Date: "+ headers["Date"]()+"\r\n"
    response_headers += "Server: "+ headers["Server"] + "\r\n"
    response_headers += "Last-Modified: "+ headers["Last-Modified"](filename) +"\r\n"
    response_headers += "ETag: "+ headers["ETag"](filename) + "\r\n"
    response_headers += "Accept-Ranges: "+ headers["Accept-Ranges"]+"\r\n"
    # response_headers += "Content-Encoding: "+ headers["Content-Encoding"] + "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+ "\r\n"
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    #if "Cookie" in request:
    #    if False:  
    #        pass
    #    else:
    #        response_headers += set_cookies() + "\r\n"           
    #else:
    #response_headers += set_cookies() + "\r\n";
    #response_headers += set_cookies() + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"\r\n"
    return (status_line + response_headers + "\r\n").encode()

def statusCode_201(filename):
    status_line = "HTTP/1.1 "+ "201 Created"+ "\r\n"
    response_headers = "Date: "+ headers["Date"]()+ "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "ETag: "+ headers["ETag"](filename)+"\r\n"
    response_headers += "Content-Location: " + filename + "\r\n"
    if "Connection: close" in request:
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive"+"\r\n"
    return (status_line + response_headers+"\r\n").encode()

def statusCode_204(filename):
    status_line = "HTTP/1.1 "+ "204 No Content"+ "\r\n"
    response_headers = "Date: "+ headers["Date"]()+ "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "ETag: "+ headers["ETag"](filename)+"\r\n"
    if "Connection: close" in request: 
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive"+"\r\n"
    return (status_line + response_headers + "\r\n").encode()

def statusCode_206(filename,start,end):
    status_line = "HTTP/1.1 "+ "206 Partial Content" + "\r\n"
    response_headers = "Date: "+ headers["Date"]()+"\r\n"
    response_headers += "Server: "+ headers["Server"]+"\r\n"
    response_headers += "Last-Modified: "+ headers["Last-Modified"](filename)+"\r\n"
    response_headers += "Content-Range: bytes "+ str(start)+"-"+str(end)+"/"+cont_length(filename)+"\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+ "\r\n"
    if "Connection: close" in request:
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive"+"\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"\r\n"
    return (status_line + response_headers + "\r\n").encode()

def statusCode_304(filename):
    status_line = "HTTP/1.1 "+ "304 Not Modified"+ "\r\n" 
    response_headers = "Date: "+ headers["Date"]()+ "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Last-Modified: "+ headers["Last-Modified"](filename) +"\r\n"
    if "Connection: close" in request:
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive"+"\r\n"
    response_headers += "ETag: "+ headers["ETag"](filename) + "\r\n"
    return (status_line + response_headers).encode()

def statusCode_403():
    status_line = "HTTP/1.1 "+ "403 Forbidden"+ "\r\n"
    filename = "forbidden.html"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]()+ "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    response_headers += "Connection: close"+"\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers+"\r\n"+ response_body+ "\r\n").encode()

def statusCode_404():
    status_line = "HTTP/1.1 " + "404 Not Found"+ "\r\n"
    filename = "Not_Found.html"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]()+ "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers+"\r\n"+ response_body+'\r\n').encode()

def statusCode_405():
    status_line = "HTTP/1.1 " + "405 Method Not Allowed" + "\r\n"
    filename = "Not_allowed.html"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Allow: GET, HEAD, POST, PUT, DELETE"+"\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers +"\r\n"+ response_body+ '\r\n').encode()

def statusCode_412():
    status_line = "HTTP/1.1 " + "412 Precondition Failed" + "\r\n"
    filename = "precondition.html"
    with open(filename, 'r') as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename) + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    response_headers += "Connection: close" + "\r\n"
    return (status_line + response_headers +'\r\n' +response_body+'\r\n').encode()

def statusCode_413():
    status_line = "HTTP/1.1 " + "413 Payload Too Large" + "\r\n"
    filename = 'payload.html'
    with open(filename, 'r') as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename) + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    response_headers += "Connection: close" + "\r\n"
    return (status_line + response_headers +'\r\n' +response_body+'\r\n').encode()

def statusCode_414():
    status_line = "HTTP/1.1 " + "414 URI Too Long" + "\r\n"
    filename = "uri.html"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    response_headers += "Connection: close"+"\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers +"\r\n"+ response_body+ '\r\n').encode()

def statusCode_415():
    status_line = "HTTP/1.1 " + "415 Unsupported Media Type"+ "\r\n"
    filename = "media.html"
    with open(filename, 'r') as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers +"\r\n"+ response_body+ '\r\n').encode()

def statusCode_416():
    status_line = "HTTP/1.1 "+ "416 Range Not Satisfiable"+"\r\n"
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Range: bytes "+ "*/"+str(cont_length(filename))+"\r\n" 
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    return (status_line + response_headers + "\r\n").encode()

def statusCode_501():
    status_line = "HTTP/1.1 "+ "501 Not Implemented" + "\r\n"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: " + headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+ "\r\n"
    if "Connection: close" in request :
       response_headers += "Connection: close"+"\r\n"
    else:
       response_headers += "Keep-Alive: "+ headers["Keep-Alive"]+"\r\n"
       response_headers += "Connection: Keep-Alive" + "\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers + response_body + "\r\n").encode()

def statusCode_503():
    status_line = "HTTP/1.1 " + "503 Service Unavailable" + "\r\n"
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Connection: close"+"\r\n"
    return (status_line + response_headers +'\r\n').encode()

def statusCode_505():
    status_line = "HTTP/1.1 " + "505 HTTP Version Not Supported" + "\r\n"
    filename = "version.html"
    with open(filename, "r") as fp:
        response_body = fp.read()
        fp.close()
    response_headers = "Date: "+ headers["Date"]() + "\r\n"
    response_headers += "Server: "+ headers["Server"]+ "\r\n"
    response_headers += "Content-Length: "+ headers["Content-Length"](filename)+"\r\n"
    response_headers += "Connection: close"+"\r\n"
    response_headers += "Content-Type: "+ headers["Content-Type"](filename)+"; charset=iso-8859-1"+"\r\n"
    return (status_line + response_headers +"\r\n"+ response_body+ '\r\n').encode()

def methods(request):
    try:
        k = request.index("HTTP")
    except:
        return statusCode_505()
    if(request[k:k+len(HTTP_Version)] != HTTP_Version):
        return statusCode_505()
    if (request[:3]=="GET" or request[:4]=="HEAD"):
        if(request[:3]=="GET"):
            req="GET"
        else:
            req="HEAD"
        j = 0
        for i in request[len(req)+2:]:
            if(i == " "):
                break
            j+=1
        filename = request[len(req)+2:j+len(req)+2]
        if(len(filename) > MAX_URI_LEN):
            return statusCode_414()
        if(content_type(filename)==None):
            return statusCode_415()
        if(os.path.exists(filename)):
            if not (os.access(filename, os.R_OK)):
                return statusCode_403()
            with open(filename,"rb") as fp:
                response_body = fp.read()
                fp.close
            if("If-None-Match" in request) and ("If-Modified-Since" in request) : #check using etag
                if(getEtag(filename)==header_val(request,'If-None-Match') and last_modify(filename)==header_val(request,"If-Modified-Since")) :
                    response = statusCode_304(filename)
                    return response
            if("Range" in request):
                value = (header_val(request, "Range")).split("=")
                if(value[0].lower() == "bytes"):
                    start = value[1].split("-")[0]
                    end = value[1].split('-')[1]
                    if(start!=''):
                        start = int(start)
                    if(end!=""):
                        end = int(end)
                    total = int(cont_length(filename))
                    with open(filename, 'rb') as fp:
                        if(start!="" and end!=""):
                            fp.seek(start,0)
                            if(start < end):
                                data = fp.read(end-start+1)
                            else:
                                return statusCode_416()
                        elif(start=="" and end!=""):
                            fp.seek(total-end,0)
                            data = fp.read(end)
                        elif(start!="" and end==''):
                            fp.seek(start,0)
                            data = fp.read(total-start+1)
                        else:
                            return statusCode_416()
                    response = statusCode_206(filename, start, end)
                    return response + data
            response = statusCode_200(filename)
            if(request[:4] == "HEAD"):
                return response + ('\r\n').encode()
            return response + response_body + "\r\n".encode()
        else:
            response = statusCode_404()
            return response

    elif(request[:4] == "POST"):      
        body = request[request.index("\r\n\r\n")+2:]
        #if(sys.getsizeof(body) > MAX_PAYLOAD):
        if (len(body)> MAX_PAYLOAD):
            return statusCode_413()
        count=0
        for ch in body:
            if(ch=='&'):
                count+=1
        details = {}
        for k in range(count+1):
            details[urllib.parse.parse_qsl(body)[k][0]] = urllib.parse.parse_qsl(body)[k][1]
        j = 0
        for i in request[6:]:
            if(i==' '):
                break
            j+=1
        filename = request[6:6+j]+".txt"
        if(len(filename) > MAX_URI_LEN):
            return statusCode_414()
        if "If-Unmodified-Since" in request:
            if not (header_val(request,"If-Unmodified-Since") == last_modify(filename)):
                return statusCode_412()
        if(os.path.exists(filename)):
            with open(filename, 'a') as fp:
                for key, value in details.items():
                    fp.write('%s : %s\n' % (key, value))
                response = statusCode_200(filename)
                with open(filename,'rb') as fp:
                    response_body = fp.read()
                    fp.close()
            return response + response_body
        else:
            with open(filename, "w") as fp:
                for key, value in details.items():
                    fp.write('%s : %s\n' % (key, value))
            response = statusCode_201(filename)
            return response
        
    elif(request[:3] == "PUT"):
        body = request[request.index("\r\n\r\n"):]
        if(sys.getsizeof(body) > MAX_PAYLOAD):
            return statusCode_413()
        j = 0
        for i in request[5:]:
            if(i == " "):
                break
            j+=1
        filename = request[5:5+j]
        if(len(filename) > MAX_URI_LEN):
            return statusCode_414()
        if(content_type(filename)==None):
            return statusCode_415()
        elif(os.path.exists(filename)):
            #if not (os.access(filename, os.W_OK)):
            #    return statusCode_403()
            with open(filename,"w") as fp:
                fp.write(body)
            response = statusCode_204(filename)  #No Content
            return response
        elif not (os.path.exists(filename)):  
            #if not (os.access(filename, os.W_OK)):
            #    return statusCode_403()
            with open(filename, "w") as fp:
                fp.write(body)
            response = statusCode_201(filename)  #Created
            return response 
        else:
            return statusCode_404()
    elif(request[:6] == "DELETE"):
        j = 0
        for i in request[8:]:
            if(i == " "):
                break
            j+=1
        filename = request[8:j+8]
        with open("deleted.html","rb") as fp:
            response_body = fp.read()
            fp.close()
        if(os.path.exists(filename)):
            try:
                os.remove(filename)
                filename = "deleted.html"
                response = statusCode_200(filename)
                return response + response_body + "\r\n".encode()
            except:
                return statusCode_403()
        else:
            response = statusCode_404()
            return response
    else:
        return statusCode_501()
        
def threaded_server():
    response = methods(request)
    connection.send(response)
    connection.close()
    return
   
headers = {
    'Date': date_time,
    'Server': 'http-server',
    'Last-Modified': last_modify,
    'Keep-Alive': 'timeout=5, max=100', 
    'ETag': getEtag,
    'Accept-Ranges': 'bytes',
    'Content-Encoding': 'gzip',
    'Content-Length': cont_length,
    'Connection': 'Keep-Alive',
    'Content-Type': content_type
}

serverPort = int(sys.argv[1])
connection_socket = socket(AF_INET, SOCK_STREAM)
connection_socket.bind(('', serverPort))
connection_socket.listen(5)
connection_list = []
print("Server is ready")
while True:
    connection, addr = connection_socket.accept()
    try:
        request = connection.recv(2048).decode()
    except:
        response = statusCode_500
        connection.send(response)
    connection_list += [connection]
    if(len(connection_list) == MAX_CONN):
        response = statusCode_503()
        connection.send(response)
        connection_list = []
    try :
        thread = Thread(target=threaded_server,args=())
        thread.start()
    except:
        pass
