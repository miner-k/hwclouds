#coding=utf-8


import  requests


username = "***********"
password = "***********"

def get_Token(username,password,region='cn-north-1'):
    """
    获取token
    :param username: 用户名
    :param password: 密码
    :param region: 区域
    :return: tokend的值
    """
    url = 'https://ecs.'+ region +'.myhwclouds.com/v3/auth/tokens'


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
              "project": {
                "name": region

              }
            }
          }
        }


    r = requests.post(url,json=data,headers=headers)
    #print r.headers
    return r.headers['X-Subject-Token']
   

if __name__ ==  '__main__':

    print get_Token(username,password)
