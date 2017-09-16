#coding=utf-8

import vpc_token
import requests

#账号和密码
username = "***********"
password = "***********"

#项目ID和查询的区域

area = ('cn-north-1','cn-south-1','cn-east-2')
project_set = {'cn-north-1':'52fb7d7429d04068ae8ff9632106e701','cn-south-1':'ee766306d2ad4387a56a0e31172185b5','cn-east-2':'21275af600cd4305840e5d10a500ee87'}

#选择对应的区域
region = area[1]
project_id = project_set[region]

host = 'https://vpc.'+ region +'.myhwclouds.com'

#获取token
tokens = vpc_token.get_Token(username, password,region)
headers = {'X-Auth-Token':tokens}


def listVPC():
    '''
    列出所有的VPC的名称和ID
    :return: 一个字典（VPC名称：VPC）
    '''
    url = host + '/v1/' + project_id + '/vpcs'

    r = requests.get(url, headers=headers)
    comp = r.json()

    vpcSet = comp["vpcs"]
    vpcDir = {}
    for vpc in vpcSet:
        vpcDir[vpc['name']] = vpc['id']

    return vpcDir

if __name__ == '__main__':
    print listVPC()