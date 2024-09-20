import httpx
import base64
from dotenv import load_dotenv
import os
import re
import hashlib

load_dotenv()

class GlobalONT:
    def __init__(self):
        self.default_cookie = {'Cookie': 'body:Language:english:id=-1'}
        self.default_data = {
            'UserName': os.getenv('ONT_USERNAME'),
            'PassWord': base64.b64encode(os.getenv('ONT_PASSWORD').encode('UTF-8')).decode("UTF-8"),
        }
        self.requests = httpx.Client(verify=False, headers=None,timeout=20)


class ONTVersion494EV3R016C10S150(GlobalONT):
    def __str__(self):
        return """
        Данный класс работает с ont 
        H8245H "ont_version": "494.E", "main_soft_v": "V3R016C10S150",
        H8245H "ont_version": "494.E", "main_soft_v": "V3R016C10S135",
        """
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.get_token(url=self.url)
        self.get_cookie(url=self.url)
        self.disable_wan_ports(url=self.url)
        self.disable_lan_ports(url=self.url)

    def get_token(self, url):
        url_get_round = "https://" + url + ":80/asp/GetRandCount.asp"
        self.token = self.requests.request(method='POST', url=url_get_round).text


    def get_cookie(self,url):
        self.default_data.update({'x.X_HW_Token' : self.token.lstrip('\ufeff')})
        url_login_cgi = "https://" + url + ":80/login.cgi"
        self.cookie = self.requests.request(method='POST', url=url_login_cgi, data=self.default_data, cookies=self.default_cookie).cookies.get('Cookie')

    def disable_wan_ports(self, url):
        # Передаем в PARAMS для отключения в секции WAN портов 2 и 4
        disable_wan_params = {
            'y': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
            'j': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
            'r': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
        }

        # Передаем в DATA для отключения в секции WAN портов 2 и 4
        disable_wan_data = {
            'y.Enable': '1',
            'y.X_HW_IPv4Enable': '1',
            'y.X_HW_IPv6Enable': '0',
            'y.X_HW_IPv6MultiCastVLAN': '-1',
            'y.X_HW_SERVICELIST': 'INTERNET',
            'y.X_HW_ExServiceList': '',
            'y.X_HW_VLAN': '200',
            'y.X_HW_PRI': '0',
            'y.X_HW_PriPolicy': 'Specified',
            'y.X_HW_DefaultPri': '0',
            'y.ConnectionType': 'IP_Bridged',
            'y.X_HW_MultiCastVLAN': '4294967295',
            'y.X_HW_BindPhyPortInfo': 'SSID1',
            'x.X_HW_Token': None,
        }

        hwtoken_url = "https://" + url + ":80/html/bbsp/wan/wan.asp"
        disable_wan_url = "https://" + url + ":80/html/bbsp/wan/complex.cgi"
        update_token = self.requests.request(method='GET', url=hwtoken_url).text
        math_hwtoken = re.search(r'hwonttoken" value="(\S+)"',update_token).group(1)
        disable_wan_data.update({'x.X_HW_Token': math_hwtoken})
        responce = self.requests.request(method='POST',url=disable_wan_url, params=disable_wan_params, data=disable_wan_data)
        if responce.status_code == 200:
            print(f"IP: {url} section WAN 2 and 4 offile")
        else:
            print(f"IP: {url} section WAN 2 and 4 ERROR")

    def disable_lan_ports(self, url):
        disable_lan_params = {
            'LAN1': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.1',
            'LAN2': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.2',
            'LAN3': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.3',
            'LAN4': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.4',
        }

        disable_lan_data = {
            'LAN1.X_HW_L3Enable': '0',
            'LAN2.X_HW_L3Enable': '0',
            'LAN3.X_HW_L3Enable': '0',
            'LAN4.X_HW_L3Enable': '0',
            'x.X_HW_Token': None,
        }

        hwtoken_url = "https://" + url + ":80/html/bbsp/layer3/layer3.asp"
        disable_lan_url = "https://" + url + ":80/html/bbsp/layer3/set.cgi"
        update_token = self.requests.request(method='GET', url=hwtoken_url).text
        math_hwtoken = re.search(r'hwonttoken" value="(\S+)"', update_token).group(1)
        disable_lan_data.update({'x.X_HW_Token': math_hwtoken})
        responce = self.requests.request(method='POST',url=disable_lan_url, params=disable_lan_params, data=disable_lan_data)
        if responce.status_code == 200:
            print(f"IP: {url} section LAN 2 and 4 offile")
        else:
            print(f"IP: {url} section LAN 2 and 4 ERROR")

# class ONTVersion494EV3R015C10S120(GlobalONT):
#     def __init__(self, url):
#         super().__init__()
#         self.url = url
#         self.get_token(url=self.url)
#         self.get_cookie(url=self.url)
#         self.disable_wan_ports(url=self.url)
#         # self.disable_lan_ports(url=self.url)
#
#     def get_token(self, url):
#         url_get_round = "https://" + url + ":80/asp/GetRandCount.asp"
#         self.token = self.requests.request(method='POST', url=url_get_round).text
#
#     def get_cookie(self,url):
#         cookies = {'Cookie': "UserName:" + self.default_data.get('UserName') + ":PassWord:" + self.default_data.get('PassWord') + ":Language:english:id=-1"}
#         data = {'x.X_HW_Token' : self.token.lstrip('\ufeff')}
#         url_login_cgi = "https://" + url + ":80/login.cgi"
#         self.cookie = self.requests.request(method='POST', url=url_login_cgi, data=data, cookies=cookies).cookies.get('Cookie')
#
#     def disable_wan_ports(self, url):
#         # Передаем в PARAMS для отключения в секции WAN портов 2 и 4
#         disable_wan_params = {
#             'y': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
#             'j': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
#             'r': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
#         }
#
#         # Передаем в DATA для отключения в секции WAN портов 2 и 4
#         disable_wan_data = {
#             'y.Enable': '1',
#             'y.X_HW_IPv4Enable': '1',
#             'y.X_HW_IPv6Enable': '0',
#             'y.X_HW_IPv6MultiCastVLAN': '-1',
#             'y.X_HW_SERVICELIST': 'INTERNET',
#             'y.X_HW_ExServiceList': '',
#             'y.X_HW_VLAN': '200',
#             'y.X_HW_PRI': '0',
#             'y.X_HW_PriPolicy': 'Specified',
#             'y.X_HW_DefaultPri': '0',
#             'y.ConnectionType': 'IP_Bridged',
#             'y.X_HW_MultiCastVLAN': '4294967295',
#             'y.X_HW_BindPhyPortInfo': 'SSID1',
#             'x.X_HW_Token': None,
#         }
#
#         hwtoken_url = "https://" + url + ":80/html/network/wan.asp "
#         disable_wan_url = "https://" + url + ":80//html/network/complex.cgi"
#         update_token = self.requests.request(method='GET', url=hwtoken_url).text
#         math_hwtoken = re.search(r'hwonttoken" value="(\S+)"', update_token).group(1)
#         disable_wan_data.update({'x.X_HW_Token': math_hwtoken})
#         response = self.requests.request(method='POST', url=disable_wan_url, params=disable_wan_params,
#                                          data=disable_wan_data)
#         if response.status_code == 200:
#             print(f"IP: {url} section WAN 2 and 4 offile")
#         else:
#             print(f"IP: {url} section WAN 2 and 4 ERROR")



class ONTVersion130DC600(GlobalONT):
    # "equipment_id": "245", "main_soft_v": "V1R006C00S122","ont_version": "130DC600"}
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.get_cookie(url=self.url)
        self.disable_wan_ports(url=self.url)
        self.disable_lan_ports(url=self.url)

    def get_cookie(self, url):
        url_login = "http://" + url + "/"
        login_cgi = url_login + 'login.cgi'
        req_login = self.requests.request(method='GET', url=url_login).text
        match_cnt = re.search(r'function GetRandCnt\(\) { return\s+(\d+)',req_login,re.M).group(1)
        getroundcnt = hashlib.md5(match_cnt.encode()).hexdigest()
        usernamecnt = hashlib.md5((os.getenv('ONT_USERNAME') + match_cnt).encode()).hexdigest()
        passwordcnt = hashlib.md5((str(hashlib.md5(os.getenv('ONT_PASSWORD').encode()).hexdigest()) + match_cnt).encode()).hexdigest()
        getcookies = {"Cookie": "tid=" + getroundcnt + usernamecnt + passwordcnt + ":" + "Language:" + "english" + ":" + "id=-1;path=/"}
        set_cookies = self.requests.request(method='GET', url=login_cgi, cookies=getcookies).cookies

    def disable_wan_ports(self, url):
        disable_wan_url = "http://" + url + "/html/network/set.cgi"
        params = {
            'y': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
            'z': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.X_HW_LANBIND',
            'j': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.X_HW_IPv6.DSLite',
            # 'RequestFile': 'html/network/confirm_wan_cfg_info.html',
        }
        data = {
            'y.Enable': '1',
            'y.X_HW_IPv4Enable': '1',
            'y.X_HW_IPv6Enable': '0',
            'y.X_HW_IPv6MultiCastVLAN': '4294967295',
            'y.X_HW_SERVICELIST': 'INTERNET',
            'y.X_HW_VLAN': '200',
            'y.X_HW_PRI': '0',
            'y.X_HW_PriPolicy': 'Specified',
            'y.X_HW_DefaultPri': '0',
            'y.ConnectionType': 'IP_Bridged',
            'y.X_HW_MultiCastVLAN': '4294967295',
            'z.Lan1Enable': '0',
            'z.Lan2Enable': '0',
            'z.Lan3Enable': '0',
            'z.Lan4Enable': '0',
            'z.SSID1Enable': '1',
            'z.SSID2Enable': '0',
            'z.SSID3Enable': '0',
            'z.SSID4Enable': '0',
        }
        responce = self.requests.request(method='POST', url=disable_wan_url, params=params, data=data)
        if responce.status_code == 200:
            print(f"IP: {url} section WAN 2 and 4 offile")
        else:
            print(f"IP: {url} section WAN 2 and 4 ERROR")

    def disable_lan_ports(self, url):
        disable_lan_url = "http://" + url + "/html/network/set.cgi"
        params = {
            'LAN1': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.1',
            'LAN2': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.2',
            'LAN3': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.3',
            'LAN4': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.4',
            # 'RequestFile': 'html/network/layer3.asp',
        }
        data = {
            'LAN1.X_HW_L3Enable': '0',
            'LAN2.X_HW_L3Enable': '0',
            'LAN3.X_HW_L3Enable': '0',
            'LAN4.X_HW_L3Enable': '0',
        }
        responce = self.requests.request(method='POST', url=disable_lan_url, params=params, data=data)
        if responce.status_code == 200:
            print(f"IP: {url} section LAN 2 and 4 offile")
        else:
            print(f"IP: {url} section LAN 2 and 4 ERROR")


class ONTVersion130AC422(GlobalONT):
    def __init__(self,url):
        super().__init__()
        self.url = url
        self.get_cookie(url=self.url)
        self.disable_wan_ports(url=self.url)
        self.disable_lan_ports(url=self.url)

    def get_cookie(self, url):
        url_login = "http://" + url + "/"
        login_cgi = url_login + 'login.cgi'
        req_login = self.requests.request(method='GET', url=url_login).text
        match_cnt = re.search(r'function GetRandCnt\(\) { return\s+(\d+)',req_login,re.M).group(1)
        getroundcnt = hashlib.md5(match_cnt.encode()).hexdigest()
        usernamecnt = hashlib.md5((os.getenv('ONT_USERNAME') + match_cnt).encode()).hexdigest()
        passwordcnt = hashlib.md5((str(hashlib.md5(os.getenv('ONT_PASSWORD').encode()).hexdigest()) + match_cnt).encode()).hexdigest()
        getcookies = {"Cookie": "tid=" + getroundcnt + usernamecnt + passwordcnt + ":" + "Language:" + "english" + ":" + "id=-1;path=/"}
        set_cookies = self.requests.request(method='GET', url=login_cgi, cookies=getcookies).cookies

    def disable_wan_ports(self, url):
        disable_wan_url = "http://" + url + "/html/network/set.cgi"
        disable_wan_params = {
            'y': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1',
            'z': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.X_HW_LANBIND',
            'j': 'InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.X_HW_IPv6.DSLite',
            # 'RequestFile': 'html/network/confirm_wan_cfg_info.html',
        }
        disable_wan_data = {
            'y.Enable': '1',
            'y.X_HW_IPv4Enable': '1',
            'y.X_HW_IPv6Enable': '0',
            'y.X_HW_IPv6MultiCastVLAN': '4294967295',
            'y.X_HW_SERVICELIST': 'INTERNET',
            'y.X_HW_VLAN': '200',
            'y.X_HW_PRI': '0',
            'y.X_HW_PriPolicy': 'Specified',
            'y.X_HW_DefaultPri': '0',
            'y.ConnectionType': 'IP_Bridged',
            'y.X_HW_MultiCastVLAN': '4294967295',
            'z.Lan1Enable': '0',
            'z.Lan2Enable': '0',
            'z.Lan3Enable': '0',
            'z.Lan4Enable': '0',
            'z.SSID1Enable': '1',
            'z.SSID2Enable': '0',
            'z.SSID3Enable': '0',
            'z.SSID4Enable': '0',
            'x.X_HW_Token': None,
        }
        hwtoken_url = "http://" + url + "/html/network/wan.asp"
        disable_wan_url = "http://" + url + "/html/network/set.cgi"
        update_token = self.requests.request(method='GET', url=hwtoken_url).text
        math_hwtoken = re.search(r'hwonttoken" value="(\S+)"', update_token).group(1)
        disable_wan_data.update({'x.X_HW_Token': math_hwtoken})
        responce = self.requests.request(method='POST', url=disable_wan_url, params=disable_wan_params,
                                        data=disable_wan_data)
        if responce.status_code == 200:
            print(f"IP: {url} section WAN 2 and 4 offile")
        else:
            print(f"IP: {url} section WAN 2 and 4 ERROR")

    def disable_lan_ports(self, url):
        disable_lan_params = {
            'LAN1': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.1',
            'LAN2': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.2',
            'LAN3': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.3',
            'LAN4': 'InternetGatewayDevice.LANDevice.1.LANEthernetInterfaceConfig.4',
            # 'RequestFile': 'html/network/layer3.asp',
        }
        disable_lan_data = {
            'LAN1.X_HW_L3Enable': '0',
            'LAN2.X_HW_L3Enable': '0',
            'LAN3.X_HW_L3Enable': '0',
            'LAN4.X_HW_L3Enable': '0',
            'x.X_HW_Token': None,
        }
        hwtoken_url = "http://" + url + "/html/network/layer3.asp"
        disable_lan_url = "http://" + url + "/html/network/set.cgi"
        update_token = self.requests.request(method='GET', url=hwtoken_url).text
        math_hwtoken = re.search(r'hwonttoken" value="(\S+)"', update_token).group(1)
        disable_lan_data.update({'x.X_HW_Token': math_hwtoken})
        responce = self.requests.request(method='POST', url=disable_lan_url, params=disable_lan_params, data=disable_lan_data)
        if responce.status_code == 200:
            print(f"IP: {url} section LAN 2 and 4 offile")
        else:
            print(f"IP: {url} section LAN 2 and 4 ERROR")
