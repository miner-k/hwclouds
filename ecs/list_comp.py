#coding=utf-8

import ecs_token
import requests

#账号和密码
username = "hwcloudsom1"
password = "Hws@123456?"

#项目ID和查询的区域

area = ('cn-north-1','cn-south-1','cn-east-2')
project_set = {'cn-north-1':'52fb7d7429d04068ae8ff9632106e701','cn-south-1':'ee766306d2ad4387a56a0e31172185b5','cn-east-2':'21275af600cd4305840e5d10a500ee87'}

#选择对应的区域
region = area[1]
project_id = project_set[region]

host = 'https://ecs.'+ region +'.myhwclouds.com'

#获取token
tokens = ecs_token.get_Token(username, password,region)
headers = {'X-Auth-Token':tokens}




def list_all_servers (project_id):
    """
    列出所有的服务器的名称和ID
    :param project_id:  项目ID
    :return:
    """

    url = host + '/v2/'+ project_id +'/servers'

    r = requests.get(url,headers=headers)
    comp = r.json()


    for server in comp.get("servers"):
        print server.get('name'),server.get('id')



if __name__ == '__main__':
    list_all_servers(project_id)