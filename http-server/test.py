import webbrowser
import sys
import requests

server_port = int(sys.argv[1])
req_uri = "http://127.0.0.1:" + str(server_port)

#Testing Simple GET request

print("--GET request-- \n")
try:
    response = requests.get(req_uri + '/index.html')
    if response:
        print("Status Code for the response : " + str(response.status_code)+'\n')
        print("Response Headers : ")
        print(response.headers)
        print("Message Body : ")
        print(response.text + '\n')
    else:
        print("An error occured\n")
except:
        print("Something went wrong\n")

#Testing POST request

print("\n--Post request--\n")
try :
    response = requests.post(req_uri + "/post", data = {'Name':'Chaitanya', 'mis':'3028'})
    if response :
        print("Status Code for response : " + str(response.status_code) + '\n')
        print("Response Headers : ")
        print(response.headers)
        print("Message Body : \n")
        print(response.text + '\n')
    else:
        print("An error occured\n")
except:
    print("Something went wrong\n")

#Testing PUT request

print("--PUT request--\n")

with open("headers.txt", "r") as fp:
    file_data = fp.read()
    fp.close()
#payload = "According to the HTTP specification, POST, PUT, and the less common PATCH requests pass their data through the message body rather than through parameters in the query string. Using requests, you’ll pass the payload to the corresponding function’s data parameter."
response = requests.put(req_uri+'/tmp/new.txt', data=file_data)
try:
    if response:
        print("Status Code : " + str(response.status_code) + "\n")
        print("Response Headers : ")
        print(response.headers)
        print(response.text)
    else:
        print("Error Occured\n")
except:
    print("Something went wrong\n")


#Testing HEAD
print("--HEAD request--\n")
try:
    response = requests.head(req_uri + '/index.html')
    if response:
        print("Status Code : " + str(response.status_code)+'\n')
        print("Response Headers : ")
        print(response.headers)
        print("Message Body : \n")
        print(response.text + '\n')
    else:
        print("An error occured\n")
except:
        print("Something went wrong\n")

def printer(response):
    if response:
        print("Status Code for the response : " + str(response.status_code)+'\n')
        print("Response Headers : ")
        print(response.headers)
        print("Message Body : ")
        print(response.text + '\n')
    else:
        print("An error occured\n")

#Status Codes for GET

#206
headers={"Range":"bytes=10-20"}
try:
    response = requests.get(req_uri + "/index.html", headers=headers)
    printer(response)
except:
        print("Something went wrong\n")

#304
headers={
        "If-None-Match":"1635915994.0410342147",
        "If-Modified-Since":"Wed, 3 Nov 2021 10:36:34 GMT"
        }
try:
    response = requests.get(req_uri + "/index.html", headers=headers)
    printer(response)
except:
        print("Something went wrong\n")

#403
try:
    response = requests.get(req_uri + "/file.txt")
    print("Status Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")

#404
try:
    response = requests.get(req_uri + "/abc.html")
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")

#414
try:
    response = requests.get(req_uri + "/dsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfndsnfjnwefnwjnfnfsnfmnfnsdsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfndsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfn.html")
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")

#415
try:
    response = requests.get(req_uri + "/abc.hmtl")
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")


#Status Codes for POST

#412
headers = {
        "If-Unmodified-Since":"Sun, 14 Nov 2021 13:20:4 GMT"
        }
try:
    response = requests.post(req_uri + "/unmod",headers=headers,data = {'Name':'Chaitanya', 'mis':'3028'})
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")

#413
try:
    data={'nre&name=Chaitanya&name=mehere&':'name=Chaitanya&ere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya&name=mehere&name=Chaitanya'}
    response = requests.post(req_uri + "/post",headers=headers,data = data)
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")

#414
try:
    response = requests.post(req_uri + "/dsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfndsnfjnwefnwjnfnfsnfmnfnsdsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfndsandadafnwefefnfnwfnjwnfjwnndfndsfnnfdsnfiewinfwenfnfndsfn.html",data={'Name':'Chaitanya'})
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
        print("Something went wrong\n")

#201
try :
    response = requests.post(req_uri + "/newpost", data = {'Name':'Chaitanya', 'mis':'3028'})
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")


#Status Codes for PUT
print("--Status Codes for PUT--\n")
#201
try :
    response = requests.put(req_uri + "/newcreate.txt", data = {'Name':'Chaitanya', 'mis':'3028'})
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")

#204
try :
    response = requests.put(req_uri + "/newcreate.txt", data = {'Name':'Chaitanya', 'mis':'3028'})
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")

#Status Codes for DELETE
print("--Status Codes for DELETE--\n")

#200
try :
    response = requests.delete(req_uri + "/newcreate.txt")
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")

#400
#200
try :
    response = requests.delete(req_uri + "/newcreate.txt")
    print("\nStatus Code: " + str(response.status_code))
    print("Response Headers : ")
    print(response.headers)
except:
    print("Something went wrong\n")

#using web browser
try:
    webbrowser.open_new(req_uri + "/ss.png")
    webbrowser.open_new(req_uri + "/v.mp4")
except:
    print("Something went wrong")

