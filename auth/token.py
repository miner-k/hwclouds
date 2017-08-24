#coding=utf-8

import  requests

username = "hwcloudsom1"
password = "Hws@123456?"

def get_Token(username,password):
    url = 'https://iam.cn-north-1.myhwclouds.com/v3/auth/tokens'


    headers = {'Content-Type':'application/json;charset=utf8'}

    data = {
      "auth": {
        "identity": {
          "methods": [
            "password"
          ],
          "password": {
            "user": {
              "name": username,
              "password": password,
              "domain": {
                "name": username
              }
            }
          }
        },
        "scope": {
          "domain": {
            "name": username
          }
        }
      }
    }

    r = requests.post(url,json=data,headers=headers)
    #print r.headers
    return r.headers['X-Subject-Token']
   

if __name__ ==  '__main__':

    print get_Token(username,password)
