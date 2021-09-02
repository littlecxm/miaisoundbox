#!/usr/bin/env python3
#author:yf
#https://github.com/flying1008
import requests
import urllib
import json
import os
import base64
import hashlib
import datetime
import time
import sys

def genRequestId():
    return base64.b64encode(uuid.uuid4().bytes).decode().strip('=')

def usage():
    print("Usage:******************* ")
    print("用法:./get_ota.py <model> <channel> <verison>")
    print("    ******参数说明******")
    print("    model:LX04,X08A,X08C,X08E")
    print("    channel:release(稳定版);stable(开发版),current(??测试版？暂时没验证)")
    print("    version:你所知道的版本号,如:1.24.8(可以随便写,但不一定有包)")
    print("    Example:./get_ota.py  X08C  stable 1.24.8")

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc < 4:
        usage()
        sys.exit()
    model=argv[1]
    channel=argv[2]
    version=argv[3]
    if channel not in ['stable','current','release']:
        print("channel不正确!")
        sys.exit()
    t = time.time()
    current_time=int(round(t * 1000))
    request ='?model={0}&version={1}&channel={2}&filterID=&locale=zh_CN&time={3}&s='.format(model,version,channel,current_time)
    salt='channel={0}&filterID=&locale=zh_CN&model={1}&time={2}&version={3}&8007236f-a2d6-4847-ac83-c49395ad6d65'.format(channel,model,current_time,version)
    bytes_request=salt.encode("utf-8")
    base_request=base64.b64encode(bytes_request)
    final_s=hashlib.md5(base_request).hexdigest().upper()
    url='http://api.miwifi.com/rs/grayupgrade/v2/'
    url= url+model +request + final_s
    req =  urllib.request.Request(url)

    rsp = urllib.request.urlopen(req)
    if rsp.getcode() == 200:
        result = rsp.read().decode('utf-8')
        json_format=json.loads(result)
        if json_format.get('data') is not  None:
            print(json.dumps(json_format.get('data'),indent=2,ensure_ascii=False)) 
    else:
        print("获取失败，请检查参数")
