#coding=utf-8
"""
管理统一身份认证中的组
"""


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


def list_iam_groups():
    """
    获取统一身份认证中的组以及对应的组ID
    :return: 组以及对应的组ID组成的字典
    """

    url = 'https://iam.cn-north-1.myhwclouds.com/v3/groups'
    # url = host + '/v3/groups'
    r = requests.get(url, headers=headers)
    comp = r.json()
    group_dic = {}
    for group_name in comp.get('groups'):
        group_dic[group_name.get('name')] = group_name.get('id')

    return group_dic


def add_usertogroup(userID,groupID):
    """
    将用户添加到指定的组中
    :param userID: IAM用户ID
    :param groupID: IAM组ID
    :return:
    """
    url = 'https://iam.cn-north-1.myhwclouds.com/v3/groups/' + groupID + '/users/'+ userID
    # url = host + '/v3/groups/' + groupID + '/users/'+ userID
    r = requests.put(url, headers=headers)
    print r.status_code


if __name__ == '__main__':
    dic = list_iam_groups()
    add_usertogroup('8d39f331c66140a9b3a2bab30e8218ce','e6ca28336a934aefb09b856f026c53ad')