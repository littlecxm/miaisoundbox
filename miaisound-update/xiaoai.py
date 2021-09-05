#!/usr/bin/env python3
#https://github.com/flying1008
from aiohttp import ClientSession
import asyncio
import logging
import json
import os
import sys
import requests
import urllib
import base64
import uuid
from pathlib import Path

from miservice import MiAccount, MiNAService,gobal


firmware = '''{
    "FirmWare":[{
    "name": "小米Pro8",
    "hardware": "X08A",
    "type": "开发版",
    "version": "1.24.9",
    "link": "https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/x08a/payload_1.24.9_90df0.bin",
    "hash": "00c355fbae2104aa6051aa34893f86a5",
    "extra": "{\\"FILE_HASH\\":\\"556v2+l2mZQkStXvdNx8Lvt4hgQqkWOyfYI80b35/oo=\\",\\"FILE_SIZE\\":\\"731185073\\",\\"METADATA_HASH\\":\\"6iW70bJYkmIRTd6coVO+pm+9eLZjmiBDdfBRZIJQts8=\\",\\"METADATA_SIZE\\":\\"72341\\"}"
  },
    {
    "name": "Redmi8",
    "hardware": "X08C",
    "type": "开发版",
    "version": "1.24.8",
    "link": "https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/x08c/payload_1.24.8_c0015.bin",
    "hash": "c021d2dae1584e54e7410bc3c70c0015",
    "extra": "{\\"FILE_HASH\\":\\"NNqEL4AMcKrUKRnYS3p1PLil1uFhROGAuXetLZj2UtM=\\",\\"FILE_SIZE\\":\\"685322148\\",\\"METADATA_HASH\\":\\"L/7OCXzQ5EkLXw+qwqHhiSSPGmJe7iEvfcjT1vPcCJ4=\\",\\"METADATA_SIZE\\":\\"72282\\"}"
  },
  {
    "name": "RedmiPro8",
    "hardware": "X08E",
    "type": "开发版",
    "version": "1.24.9",
    "link": "https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/x08e/payload_1.24.9_0f400.bin",
    "hash": "603e615dab4ebe966a36b1c5e000f400",
    "extra": "{\\"FILE_HASH\\":\\"WDOaoOt4pp9ZzAyBz8y3xTwwdmN0O8J8n7lCUa6qKMk=\\",\\"FILE_SIZE\\":\\"745108921\\",\\"METADATA_HASH\\":\\"3ehZ/B7w/qNpp94jC3HTiJlcXPf/YeMdGm1KB1OXPdI=\\",\\"METADATA_SIZE\\":\\"51378\\"}"
  }]
}'''

def usage():
    print("Usage: ***********************************")
    print("         ./micli.py <ACCOUNT>   <PASSWORD>")
    print("         ACCOUNT:xiaomi account")
    print("         PASSWORD:your password\n")
    print("         Example:./micli.py 133453232 123456")

def genRequestId():
    return base64.b64encode(uuid.uuid4().bytes).decode().strip('=')
    
def update():
    headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': f"userId={gobal.get_value('userId')};serviceToken={gobal.get_value('serviceToken')};deviceId={gobal.get_value('deviceID')};sn={gobal.get_value('serialNumber')}", 
        'User-Agent': "MISoundBox/2.1.25 (com.xiaomi.mico; build:2.1.56; iOS 13.7.0) Alamofire/4.9.1 MICO/iOSApp/appStore/2.1.25"
    }

    firmware_json=json.loads(firmware)
    firmware_list = firmware_json.get('FirmWare')
    
    for obj in firmware_list:
        if gobal.get_value('hardware') == obj['hardware']:
            gobal.set_value('version',obj['version'])
            gobal.set_value('link',obj['link'])
            gobal.set_value('hash',obj['hash'])
            gobal.set_value('extra',obj['extra'])
    if gobal.get_value('hash') is None or len(gobal.get_value('hash')) == 0:
        print("暂不支持此设备的升级!")
        return 
       
    data = {
        "deviceId": gobal.get_value('deviceID'),
        "url": gobal.get_value('link'),
        "checksum": gobal.get_value('hash'),  # md5 hash
        "version": gobal.get_value('version'),
        "hardware": gobal.get_value('hardware'),
        "extra": gobal.get_value('extra'),
        "requestId": genRequestId()
    }      
    ota_api='http://api2.mina.mi.com/remote/ota/v2'
    url_encoded = urllib.parse.urlencode(data)
    # print(url_encoded)
    req =  urllib.request.Request(ota_api, headers=headers, data=url_encoded.encode('utf-8'))
    rsp = urllib.request.urlopen(req)
    print(rsp.getcode())
    print(rsp.read().decode('utf-8'))

async def main(args):
    async with ClientSession() as session:
        env = os.environ
        current=os.getcwd()
        with open(current+'\\user.ini','r') as file:
            user_file = json.loads(file.read())
        print(user_file)
        userID=user_file['user']
        password=user_file['pwd']
        file.close()
        print(userID)
        print(password)
        account = MiAccount(session, userID, password, os.path.join(str(Path.home()), '.mi.token'))
        service = MiNAService(account)
        result = await service.device_list()
        if not isinstance(result, str):
            result = json.dumps(result, indent=2, ensure_ascii=False)
        print("您选择的设备信息如下:")
        print('name:',gobal.get_value('name'))
        print('deviceID:',gobal.get_value('deviceID'))
        print('hardware:',gobal.get_value('hardware'))
        print('serialNumber:',gobal.get_value('serialNumber'))

        if gobal.get_value('name') is  not None  and gobal.get_value('deviceID') is not None and \
            gobal.get_value('hardware') is not None and  gobal.get_value('serialNumber') is not None and \
            gobal.get_value('userId') is not None  and gobal.get_value('serviceToken') is not None :
            update()
            print("press any key to exit!")
            input()

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    argi = 0
    gobal._init()

    if argc > argi:
        asyncio.get_event_loop().run_until_complete(main(' '.join(argv[argi:])))
    else:
        usage()
