#coding=utf-8

import iam_token
import requests

# 账号和密码

username = "linux_user001"
password = "543156149qq"

# 项目ID和查询的区域

area = ('cn-north-1', 'cn-south-1', 'cn-east-2')
project_set = {'cn-north-1': '52fb7d7429d04068ae8ff9632106e701', 'cn-south-1': 'ee766306d2ad4387a56a0e31172185b5',
               'cn-east-2': '21275af600cd4305840e5d10a500ee87'}

# 选择对应的区域
region = area[1]
project_id = project_set[region]

host = 'https://iam.' + region + '.myhuaweicloud.com'

# 获取token
tokens = iam_token.get_Token(username, password, region)
headers = {
    'Content-Type':'application/json;charset=utf8',
    'X-Auth-Token': tokens
    }


def list_iam_users():
    """
    显示统一身份认证中所有的用户信息
    :return:用户和用户ID组成的字典
    """

    url = host + '/v3/users'
    r = requests.get(url,headers=headers)
    comp = r.json()
    users_dic = {}
    for name in comp.get('users'):
        users_dic[name.get('name')] = name.get('id')

    return users_dic

def add_iam_user(iam_user,iam_user_pw='Jfz!955988',iam_user_email=''):
    """
    在统一身份认证中增加用户
    :param iam_user: 增加的用户名,必须要大于五个字符串
    :param iam_user_pw: 用户名对应的密码
    :param iam_user_email: 用户名对应的邮箱
    :return:
    """
    url = host + '/v3/users'
    # url = 'https://iam.cn-east-2.myhuaweicloud.com/v3/users'
    data = {
        "user": {
            "name":iam_user,
            "password":iam_user_pw,
            "email":iam_user_email
        }
        }
    r = requests.post(url,json=data, headers=headers)
    # print r.json()



if __name__ == '__main__':
    # iam_user = 'tom-ee'
    # iam_user_pw = 'test.ereeeee'
    # iam_user_email = '543156149@qq.com'
    # list_iam_users()
    # add_iam_user(iam_user,iam_user_pw,iam_user_email)
    print list_iam_users()

