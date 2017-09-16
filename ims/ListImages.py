#coding=utf-8


import requests

from ims import ims_token

#账号和密码
username = "***********"
password = "***********"

#项目ID和查询的区域

area = ('cn-north-1','cn-south-1','cn-east-2')
project_set = {'cn-north-1':'52fb7d7429d04068ae8ff9632106e701','cn-south-1':'ee766306d2ad4387a56a0e31172185b5','cn-east-2':'21275af600cd4305840e5d10a500ee87'}

#选择对应的区域
region = area[2]
project_id = project_set[region]

host = 'https://ims.'+ region +'.myhwclouds.com'


#获取token
tokens = ims_token.get_Token(username, password, region)
headers = {'X-Auth-Token':tokens}

def listImages():
    '''
     列出所有的镜像名称以及对应的ID
    :return: 字典，{镜像名称：镜像}
    '''
    url = host + '/v2/cloudimages'

    r = requests.get(url, headers=headers)
    respon = r.json()

    imageSet = {}
    for image in  respon['images']:
        imageSet[image['name']] = image['id']

    return imageSet

if __name__ == '__main__':
    set = listImages()
    print  set.keys()

