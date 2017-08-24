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



url = host + '/v1/'+ project_id +'/cloudservers'




if __name__ == '__main__':
        #list_all_servers(north_project_id)