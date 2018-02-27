#coding=utf-8

import requests
from openpyxl import workbook
from openpyxl import load_workbook

def get_Token(username, password, region):
    """
    获取token
    :param username:
    :param password:
    :param region:
    :return:
    """
    url = 'https://iam.' + region + '.myhwclouds.com/v3/auth/tokens'

    headers = {'Content-Type': 'application/json;charset=utf8'}

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

    r = requests.post(url, json=data, headers=headers)
    # print r.headers
    return r.headers['X-Subject-Token']



def list_iam_users():
    """
    显示统一身份认证中所有的用户信息
    :return:
    """

    url = host + '/v3/users'
    r = requests.get(url,headers=headers)
    comp = r.json()
    for name in comp.get('users'):
        print name.get('name')

def add_iam_user(iam_user,iam_user_pw='Jfz!955988',iam_user_email=''):
    """
    在统一身份认证中增加用户
    :param iam_user: 增加的用户名,必须要大于五个字符串
    :param iam_user_pw: 用户名对应的密码
    :param iam_user_email: 用户名对应的邮箱
    :return:
    """
    url = host + '/v3/users'
    data = {
        "user": {
            "name":iam_user,
            "password":iam_user_pw,
            "email":iam_user_email
        }
        }
    r = requests.post(url,json=data, headers=headers)
    # print r.json()

from openpyxl import load_workbook


def get_users_xls(filename):
    """
    获取表中的用户名
    :param filename:Execl表的名称
    :return: 用户名数组
    """
    wb = load_workbook(filename)
    ws = wb.active

    # 表中的第一列是用户名的拼音
    ROW = 2
    COL = 1
    USER = []
    while True:
        if ws.cell(row=ROW,column=COL).value == None:
            break

        else:
            USER.append(ws.cell(row=ROW,column=COL).value )
            ROW += 1

    return USER


if __name__ == '__main__':
    # 账号和密码(修改)
    username = "linux_user001"
    password = "543156149qq"

    # 项目ID和查询的区域（修改）
    area = ('cn-north-1', 'cn-south-1', 'cn-east-2')
    project_set = {'cn-north-1': '52fb7d7429d04068ae8ff9632106e701', 'cn-south-1': 'ee766306d2ad4387a56a0e31172185b5',
                   'cn-east-2': '21275af600cd4305840e5d10a500ee87'}

    # 选择对应的区域
    region = area[1]
    project_id = project_set[region]

    host = 'https://iam.' + region + '.myhuaweicloud.com'

    # 获取token
    tokens = get_Token(username, password, region)
    headers = {
        'Content-Type': 'application/json;charset=utf8',
        'X-Auth-Token': tokens
    }

    list_iam_users()

    for iam_user_name in get_users_xls('test.xlsx'):
        add_iam_user(iam_user_name)
    print '#' * 10
    list_iam_users()
