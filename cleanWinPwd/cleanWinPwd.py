#coding=utf-8
'''
清除windows操作系统的密码

思路：
    1.获取服务器的信息
    2.判读服务器的状态是否关机、镜像是否为windows
    3.创建Ubuntu 16的服务器
    4.卸载windows服务器的磁盘，挂载到ubuntu服务器上
    5.重新启动ubuntu服务器
    6.检测ubuntu服务器的状态
    7.卸载Ubuntu服务器的数据盘，挂载到windows服务器上
    8.挂载完成之后，重新启动windows服务器
    9.删除临时服务器

所需要的函数；
    1.获取windows服务器的信息
    2.镜像名称和ID的对应列表
    3.创建服务器
    4.挂载磁盘、卸载磁盘
    5.服务器的关机和开机
    6.删除服务器
'''
import  requests

#用户名和密码
username = "username"
password = "password"


#项目ID和查询的区域
area = ('cn-north-1','cn-south-1','cn-east-2')
project_set = {'cn-north-1':'52fb7d7429d04068ae8ff9632106e701','cn-south-1':'ee766306d2ad4387a56a0e31172185b5','cn-east-2':'21275af600cd4305840e5d10a500ee87'}

#选择对应的区域
region = area[0]
project_id = project_set[region]



#服务器的ID
win_server_id = '0b961d83-443a-48a5-89d8-8f75aa323ae3'




def get_Token(username,password):
    """
    获取token
    :param username: 用户名
    :param password: 密码
    :param region: 区域
    :return: tokend的值
    """
    url = 'https://ecs.'+ region +'.myhwclouds.com/v3/auth/tokens'


    headers = {'Content-Type':'application/json;charset=utf8'}

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
              "project": {
                "name": region

              }
            }
          }
        }


    r = requests.post(url,json=data,headers=headers)

    return r.headers['X-Subject-Token']
   

def getWinInfo(winID):
    '''
    查询服务器的操作系统、状态、VPCID、系统盘ID、
    :param winID: 需要重置密码的服务器的ID
    :param region: 服务器所有的区域
    :return: 服务器详情的字典
    '''

    # 服务器的Endpoint和URL
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v2/'+ project_id +'/servers/' + winID

    r = requests.get(url,headers=headers)
    comp = r.json()

    infoSet = {}

    infoSet['availability_zone'] = comp['server']['OS-EXT-AZ:availability_zone']
    infoSet['status'] = comp['server']['status']
    infoSet['imageID'] = comp['server']['image']['id']
    infoSet['vpcID'] = comp['server']['addresses'].keys()[0]


    return infoSet

def stoppedStatus(serverID):
    '''
    确保服务器的状态是关机状态
    :param serverID: 服务器的ID

    '''

    while True:
        infoSet = getWinInfo(serverID)
        if infoSet['status'] == 'SHUTOFF':
            break

def getSubnetID(VPCID):
    '''
    获取VPC下的一个子网ID
    :param VPCID: VPC的ID
    :return: subnetID ()
    '''

    host = 'https://vpc.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/subnets' + '?vpc_id=' + VPCID

    r = requests.get(url, headers=headers)
    comp = r.json()

    return comp['subnets'][0]['id']

def listImages():
    '''
    列出所有的镜像
    :return: 字典，{镜像名称：镜像}
    '''

    host = 'https://ims.' + region + '.myhwclouds.com'
    url = host + '/v2/cloudimages'

    r = requests.get(url, headers=headers)
    respon = r.json()

    imageSet = {}
    for image in  respon['images']:
        imageSet[image['name']] = image['id']

    return imageSet

def getOS(imageID):
    '''
    通过镜像ID判断服务器的操作系统
    :param imageID: 镜像ID
    :return: 服务器的操作系统(string)
    '''

    imageSet = listImages()

    for key in imageSet.keys():
       if imageSet[key] == imageID :
           return key
       else:
           pass

def isWin(infoSet):
    '''
    判断是否为windows操作系统
    :param infoSet:  服务器的信息
    :return: （布尔型）
    '''


    OS  = getOS(infoSet['imageID'])
    return OS.lower().startswith('windows')

def getUbuntuID():
    '''
    获取Ubuntu的镜像ID
    :return: 字符串
    '''

    imageSet = listImages()
    return imageSet['Ubuntu 16.04 server 64bit']


#创建服务器
def createServer(zone,imageID,vpcID,subnetID):
    '''
    创建一个Ubuntu服务器
    :param zone: 可用区，必须和windows服务器相同否则磁盘无法挂载
    :param imageID: ubuntud的镜像ID
    :param vpcID:  VPC的ID
    :param subnetID:  子网的ID
    :param ipType:  弹性IP的类型，5_bgp, 华南的需要设置为5_sbgp
    :return: 直接打印状态码
    '''

    if region == "cn-south-1":
        ipType = "5_sbgp"
    else:
        ipType = '5_bgp'

    # 服务器的Endpoint和URL
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/cloudservers'

    body = {
            "server": {
                "adminPass": password,
                "availability_zone": zone,
                "name": "Ubuntu临时服务器",
                "imageRef": imageID,
                "root_volume": {
                    "volumetype": "SATA"
                },
                "personality": [
                    {
                        "path": "/etc/rc.local",
                        "contents": "IyEvYmluL2Jhc2gKd2dldCBodHRwczovL2dpdGh1Yi5jb20vbWluZXItay9jbGVhcl93aW5fcHdkL2FyY2hpdmUvMC4zLnRhci5negp0YXIgLXh2ZiAwLjMudGFyLmd6CmNkIGNsZWFyX3dpbl9wd2QtMC4zCmJhc2ggY2hhbmdlX3Bhc3N3ZC5zaA=="
                    }
                ],
                "flavorRef": "c1.medium",

                "vpcid": vpcID,

                "nics": [
                    {
                        "subnet_id": subnetID
                    }
                ],
               "publicip": {

                    "eip": {
                        "iptype": ipType,
                        "bandwidth": {
                            "size": 1,
                            "sharetype": "PER"
                        }
                    }
                },

                "count": 1,

            }
        }

    r = requests.post(url, json=body, headers=headers)
    comp = r.json()
    print "创建服务器的状态：" + str(r.status_code,)

    print  comp['job_id']
    return comp['job_id']

def getNewServerID(job_id):
    '''
    通过创建服务器时返回的job_id，判断执行结果，以及返回服务器的ID
    :param job_id: 创建服务器返回的job_id
    :return: 创建的服务的ID
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/jobs/' + job_id

    r = requests.get(url, headers=headers)
    comp = r.json()
    print comp['status']
    return comp['entities']['sub_jobs'][0]['entities']['server_id']

def getJobStatus(job_id):
    '''
    通过创建服务器时返回的job_id，判断执行结果
    :param job_id: 创建服务器返回的job_id
    :return: 创建的服务的ID
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/jobs/' + job_id

    while True:
        r = requests.get(url, headers=headers)
        comp = r.json()
        #print comp
        if comp['status'] == 'SUCCESS':
            break


def getDiskID(serverID):
    '''
    通过服务器的ＩＤ获取系统盘的ＩＤ
    :param serverID: 服务器的ID
    :return: 系统盘的ＩＤ
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v2/' + project_id + '/servers/' + serverID + '/os-volume_attachments'

    r = requests.get(url, headers=headers)
    comp = r.json()

    for disk in  comp['volumeAttachments']:
        if disk['device'] == "/dev/sda":
            return disk['id']

def unloadDisk(serverID,volumeID):
    '''
    卸载磁盘
    :param serverID:服务器的ID
    :param volumeID:磁盘的ID
    :return: job_ID 通过job_id查询动作是否成功
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/cloudservers/' + serverID + '/detachvolume/' + volumeID


    r = requests.delete(url,headers=headers)
    comp = r.json()
    print "卸载磁盘"
    return comp['job_id']



def mountDisk(serverID,volumeID,mountPoint):
    '''
    挂载磁盘
    :param serverID:服务器的ID
    :param volumeID: 磁盘的ID
    :return: job_id,查看是否完成
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/cloudservers/' + serverID + '/attachvolume'

    body = {
            "volumeAttachment": {
                 "volumeId": volumeID,
                 "device": mountPoint
            }
            }
    r = requests.post(url,json=body, headers=headers)
    comp = r.json()
    print "挂载磁盘"
    return comp['job_id']


def turnoffServer(serverID):
    '''
    关闭服务器
    :param serverID: 服务器的ID
    :return:
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v2/' + project_id + '/servers/' + serverID + '/action'

    body = {
                "os-stop": {}
            }
    r = requests.post(url, json=body, headers=headers)

    return  "关闭服务器：" + str(r.status_code)


def turnonServer(serverID):
    '''
    启动服务器
    :param serverID:服务器的ID
    :return:
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v2/' + project_id + '/servers/' + serverID + '/action'

    body = {
                "os-start": {}
            }
    r = requests.post(url, json=body, headers=headers)

    return "启动服务器：" + str(r.status_code)

def restartServer(serverID):
    '''
    重新启动服务器
    :param serverID:服务器的ID
    :return:
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v2/' + project_id + '/servers/' + serverID + '/action'

    body = {
            "reboot": {
                "type": "SOFT"
            }
}
    r = requests.post(url, json=body, headers=headers)

    return "重启服务器：" + str(r.status_code)
    pass

def delServer(serverID):
    '''
    删除服务器
    :param serverID:
    :return:
    '''
    host = 'https://ecs.' + region + '.myhwclouds.com'
    url = host + '/v1/' + project_id + '/cloudservers/delete'

    data = {
        "servers": [
            {
                "id": serverID
            }
        ],
        "delete_publicip": 'true',
        "delete_volume": 'false'
    }

    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 200:
        print "删除成功"
    else:
        print "删除失败"
    pass


if __name__ ==  '__main__':

    # 获取token

    try:
        tokens = get_Token(username, password)
        headers = {'X-Auth-Token': tokens}

    except KeyError:
        print "获取Token失败，请检查用户名密码"

    else:
        # 获取服务器的信息
        winInfo = getWinInfo(win_server_id)

        # 获取系统盘的ID
        win_sys_diskID = getDiskID(win_server_id)

        # subnetID  240bb5aa-e73c-4633-9e89-420dcd2cc5b9
        subnetID = getSubnetID(winInfo['vpcID'])

        #判断服务器的操作系统
        if not isWin(winInfo):
            raise  ValueError,"输入的serverID不是windows操作系统的服务器ID，请重新输入"
        else:
            pass
        #获取Ubuntu的镜像ID
        ubuntuImageID = getUbuntuID()

        #创建Ubuntu服务器

        create_job_id = createServer(winInfo['availability_zone'],ubuntuImageID,winInfo['vpcID'],subnetID)


        # 新创建的Ubuntu的服务器的ID
        getJobStatus(create_job_id)
        UbuntServerID = getNewServerID(create_job_id)

        # 关闭windows服务器,并保证服务器时关机状态
        print turnoffServer(win_server_id)
        print stoppedStatus(win_server_id)

        # 确保Ubuntu服务器创建成功
        getJobStatus(create_job_id)

        #确保windows服务器关机成功

        # 卸载系统盘
        unload_job_id = unloadDisk(win_server_id,win_sys_diskID)
        getJobStatus(unload_job_id)

        # 挂载磁盘到Ubuntu系统
        mount_job_id = mountDisk(UbuntServerID,win_sys_diskID,'/dev/sdb')
        getJobStatus(mount_job_id)

        #重新启动Ubuntu服务器
        restartServer(UbuntServerID)

        # 保证Ubuntu服务器是关机状态
        stoppedStatus(UbuntServerID)

        # 从Ubuntu上卸载磁盘
        # win_sys_diskID = '063d002e-b39a-426d-8844-8db87ed125cd'
        unload_job_id2 = unloadDisk(UbuntServerID,win_sys_diskID)
        getJobStatus(unload_job_id2)

        # 挂载磁盘的到windows服务器上
        mount_job_id2 = mountDisk(win_server_id,win_sys_diskID,'/dev/sda')
        getJobStatus(mount_job_id2)

        # 启动windows服务器
        turnonServer(win_server_id)

        # 删除Ubuntu服务器
        delServer(UbuntServerID)


