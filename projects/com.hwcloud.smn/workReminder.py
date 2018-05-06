#coding=utf-8


import requests

def getToken():

    username = 'zhangyinkai'
    domain_name = 'hwcloudsom1'
    password = 'zYK,1410'
    project_name = "cn-north-1"
    IAM_URL = 'https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens'
    headers = {'Content-Type':'application/json;charset=utf8'}

    body = {
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
                "name": domain_name
              }
            }
          }
        },
        "scope": {
          "project": {
            "name": project_name

          }
        }
      }
    }

    r = requests.post(url=IAM_URL,json=body,headers=headers)
    # print r.status_code

    # print r.headers['X-Subject-Token']
    return r.headers['X-Subject-Token']

def sendMessages(phones,messages,sign_id = "e0cde4e0b08e4ce590344737e852abe5"):
    '''
    发送短信通知
    :param phones: 需要通知的列表
    :param messages: 通知内容
    :param sign_id: 短信签名
    :return:
    '''

    # phones = ["13323952520","13403622324"]
    # messages = "上班提醒："
    # sign_id = "e0cde4e0b08e4ce590344737e852abe5"
    SDM_URL = ' https://smn.cn-north-1.myhuaweicloud.com/v2/52fb7d7429d04068ae8ff9632106e701/notifications/sms'

    tokens = getToken()
    headers = {
        'Content-Type': 'application/json;charset=utf8',
        'X-Auth-Token': tokens
    }
    body =  {
        "endpoints": phones,
        "message": messages,
        "sign_id": sign_id
    }

    r = requests.post(url=SDM_URL,json=body,headers=headers)
    print r.status_code

if __name__ == '__main__':
    getToken()
    sendMessages(['13403622324','00642102524976'],'上班提醒')