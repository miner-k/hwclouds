#coding=utf-8

import ecs_token
import requests


username = "hwcloudsom1"
password = "Hws@123456?"

#获取token
tokens = ecs_token.get_Token(username, password)
headers = {'X-Auth-Token':tokens}

north_project_id = '52fb7d7429d04068ae8ff9632106e701'
project_id = north_project_id
host = 'https://ecs.cn-north-1.myhwclouds.com'

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
    print r.status_code

if __name__ == '__main__':
    del_server(server_id)