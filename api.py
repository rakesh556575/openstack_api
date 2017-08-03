import requests
import json
import logging
logging.basicConfig(filename="api.log", level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
def test_api(test_data):
    api = test_data["api"]
    method = test_data["method"]

    results=test_data["result"]
    params = test_data["params"]
    home_url=test_data["home_url"]
    identity_port=test_data["identity_port"]
    username=test_data["user"]
    password=test_data["password"]
    X_Auth_Token=auth_token(home_url,identity_port,username,password)

    headers = {"Content-Type": "application/json", "X-Auth-Token": X_Auth_Token}
    if method == 'get':
        try:
            logging.info("Calling Rest API Get method")
            test_get(api,headers,results)

        except Exception as e:
            logging.error("Calling Rest API failed")
            print("Eception occured :{}".format(e))
    elif method == 'post':
        try:
            logging.info("Calling Rest API Post method")
            test_post(api, headers, params, results)
        except Exception as e:
            logging.error("Calling Rest API failed")
            print("Eception occured :{}".format(e))

    elif method=="delete":
        try:
            test_delete(api,headers,results)
        except Exception as e:
            print("Eception Occured {}".format(e))






def test_get(api,headers,results):


    response = requests.get(url=api,headers=headers)
    flag=0

    data = response.json()["{}".format(results[0])]
    print(data)
    for i in data:
        for j in i:


            if i[j]==results[1]:

                flag=1

    if flag==1:
        logging.info("Test Passed")
        print("Pass")
    else:
        logging.error("Test Failed")
        print("Fail")


def test_post(api, headers, params, results):
    try:
        response = requests.post(url=api,data=json.dumps(params), headers=headers)


        results_observed = response.json()
        test_get(api,headers,results)
    except Exception as e:
        print("Exeception Occured {}".format(e))

def test_delete(api,headers,results):

    try:
       id=get_id(api,headers,results)
       api=api+"/"+id
       response=requests.delete(api,headers=headers)
       print(response)
       if response.status_code==204:
           print("Pass")
       else:
           print("Fail")
    except Exception as e:
        print("Execption Occured {}".format(e))







def auth_token(home_url,identity_port,username,password):
    token_url = home_url + ":" + str(identity_port) + "/v3/auth/tokens"

    body = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "name": "admin",
                    "domain": {
                        "name": "Default"
                    }
                }
            }
        }
    }

    try:
        response = requests.post(token_url, json=body)
        head = response.headers.items()
        logging.info("Generating Xauth-Token")
    except Exception as e:
        logging.error("generating Xauth-Token Failed")
        print("Execption occured {}".format(e))

    X_Auth_Token = ""

    for item in head:  # each item is a tuple
        if item[0] == 'X-Subject-Token':
            X_Auth_Token = item[1]
    print(X_Auth_Token)
    return X_Auth_Token


test_data = {"home_url":"http://10.103.199.192",
              "api":"http://10.103.199.192:5000/v3/projects",
             "identity_port":5000,
             "user":"admin",
            "password":"f4d110f1ca314a71",
            "method": "get",

            "result": ['projects','demo'],
            "params":0
            }

test_data2 = {"home_url":"http://10.103.199.192",
             "api":"http://10.103.199.192:5000/v3/users",
            "method": "get",
             "identity_port":5000,
             "user":"admin",

            "password":"f4d110f1ca314a71",
            "result": ['users','demo'],
            "params":0
            }


test_data3 = {"home_url":"http://10.103.199.192",
              "api":"http://10.103.199.192:8774/v2.1/servers",
             "identity_port":5000,
             "user":"admin",
            "password":"f4d110f1ca314a71",
            "method": "get",

            "result": ['servers','test'],
            "params":0
            }


test_data4={"home_url":"http://10.103.199.192",
              "api":"http://10.103.199.192:8774/v2.1/servers",
             "identity_port":5000,
             "user":"admin",
            "password":"f4d110f1ca314a71",
            "method": "post",

            "params":
                   {
                     "server" : {
                               "accessIPv4": "1.2.3.4",
                                "accessIPv6": "80fe::",
                                 "name" : "rakesh",
                                "imageRef" : "412ef8a7-1f7b-4223-8239-53ba6e975281",
                                "flavorRef" : "1",
                                "availability_zone": "nova",
                                "OS-DCF:diskConfig": "AUTO",
                                 "metadata" : {
                                 "My Server Name" : "Apache1"
                                    },
                                 "personality": [
                                    {
                                    "path": "/etc/banner.txt",
                                     "contents": "ICAgICAgDQoiQSBjbG91ZCBkb2VzIG5vdCBrbm93IHdoeSBp dCBtb3ZlcyBpbiBqdXN0IHN1Y2ggYSBkaXJlY3Rpb24gYW5k IGF0IHN1Y2ggYSBzcGVlZC4uLkl0IGZlZWxzIGFuIGltcHVs c2lvbi4uLnRoaXMgaXMgdGhlIHBsYWNlIHRvIGdvIG5vdy4g QnV0IHRoZSBza3kga25vd3MgdGhlIHJlYXNvbnMgYW5kIHRo ZSBwYXR0ZXJucyBiZWhpbmQgYWxsIGNsb3VkcywgYW5kIHlv dSB3aWxsIGtub3csIHRvbywgd2hlbiB5b3UgbGlmdCB5b3Vy c2VsZiBoaWdoIGVub3VnaCB0byBzZWUgYmV5b25kIGhvcml6 b25zLiINCg0KLVJpY2hhcmQgQmFjaA=="
                                     }
                                     ],
                                    "security_groups": [
                                     {
                                      "name": "default"
                                       }
                                      ],
                                       "user_data" : "IyEvYmluL2Jhc2gKL2Jpbi9zdQplY2hvICJJIGFtIGluIHlvdSEiCg=="
                                        },
                                 "OS-SCH-HNT:scheduler_hints": {
                                 "same_host": "48e6a9f6-30af-47e0-bc04-acaed113bb4e"
                                }
                   },

            "result":['servers','rakesh']
            }


test_data5 = {"home_url":"http://10.103.199.192",
              "api":"http://10.103.199.192:8774/v2.1/servers",

             "identity_port":5000,
             "user":"admin",
            "password":"f4d110f1ca314a71",
            "method": "delete",

            "result": ['servers','rakesh'],
            "params":0
            }
def parse(response,results):
    data = response.json().get(results[0])
    for i in data:
        for j in i:
            if [i][j]==results[1]:
                return "Present"
            else:
                return "Not Present"




def get_id(api,headers,results):
    response = requests.get(url=api, headers=headers)


    data = response.json()["{}".format(results[0])]
    for i in data:
        for j in i:


            if i[j]==results[1]:

                return i["id"]
    else:
        return None
test_api(test_data)
#test_api(test_data2)
#test_api(test_data4)
#test_api(test_data5)

