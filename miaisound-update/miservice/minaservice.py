import json
from .miaccount import MiAccount, get_random
from . import gobal 
import logging
_LOGGER = logging.getLogger(__package__)


class MiNAService:

    def __init__(self, account: MiAccount):
        self.account = account

    async def mina_request(self, uri, data=None):
        requestId = 'app_ios_' + get_random(30)
        if data is not None:
            data['requestId'] = requestId
        else:
            uri += '&requestId=' + requestId
        headers = {'User-Agent': 'MiHome/6.0.103 (com.xiaomi.mihome; build:6.0.103.1; iOS 14.4.0) Alamofire/6.0.103 MICO/iOSApp/appStore/6.0.103'}
        return await self.account.mi_request('micoapi', 'https://api2.mina.mi.com' + uri, data, headers)

    async def device_list(self, master=0):
        result = await self.mina_request('/admin/v2/device_list?master=' + str(master))
        device={}
        for index,obj in enumerate(result.get('data')):
            print("*****************")
            print ("第%d个设备信息:" % (index +1))
            print('name:',obj['name'])
            print('deviceID:',obj['deviceID'])
            print('hardware:',obj['hardware'])
            print('serialNumber:',obj['serialNumber'])
            item={
                "name":obj['name'],
                "deviceID":obj['deviceID'],
                "hardware":obj['hardware'],
                "serialNumber":obj['serialNumber']
            }
            device[index+1] = item
            print("*****************")

        print("请输入你要升级的设备序号:")
        num=input()
        for key,value in device.items():
            if int(num) == key :
                gobal.set_value('name',value['name'])
                gobal.set_value('deviceID',value['deviceID'])
                gobal.set_value('hardware',value['hardware'])
                gobal.set_value('serialNumber',value['serialNumber'])

        return "获取设备信息成功" if result else None

