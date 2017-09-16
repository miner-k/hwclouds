#coding=utf-8

import ecs_token
import requests



username = "**********"
password = "**********"


#获取token
tokens = ecs_token.get_Token(username, password)
headers = {'X-Auth-Token':tokens}

#项目ID和查询的区域

area = ('cn-north-1','cn-south-1','cn-east-2')
project_set = {'cn-north-1':'52fb7d7429d04068ae8ff9632106e701','cn-south-1':'ee766306d2ad4387a56a0e31172185b5','cn-east-2':'21275af600cd4305840e5d10a500ee87'}

#选择对应的区域
region = area[1]
project_id = project_set[region]

host = 'https://ecs.'+ region +'.myhwclouds.com'

#服务器的ID
server_id = 'd5eee123-31a5-4921-869f-5d82bf8e1dce'

def del_server(server_id,del_ip='false',del_vol='false'):
    ''' 删除服务器
        server_id:服务器的ID
        del_ip:是否删除绑定的弹性IP
        del_vol:是否删除数据盘
    '''
    url = host + '/v1/' + project_id +'/cloudservers/delete'

    data = {
        "servers": [
            {
                "id": server_id
            }
        ],
        "delete_publicip": del_ip,
        "delete_volume": del_vol
    }


    r = requests.post(url,json=data,headers=headers)
    if r.status_code == 200:
        print "删除成功"
    else:
        print "删除失败"

if __name__ == '__main__':
    del_server(server_id)
