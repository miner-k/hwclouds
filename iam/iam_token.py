
#coding=utf-8

import  requests

# <<<<<<< HEAD:auth/token.py
# username = "**********"
# password = "**********"
# =======
# username = "username"
# password = "passwd"
# >>>>>>> origin/master:iam/token.py

def get_Token(username,password,region):
    url = 'https://iam.' + region + '.myhwclouds.com/v3/auth/tokens'


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
