import requests
import httpx
from scrapli import Scrapli
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
class ConnectOLT:

    def __init__(self):
        self.OLT = {
            "host": "10.35.8.5",
            "auth_username": os.getenv("LOGIN"),
            "auth_password": os.getenv("PASSWORD"),
            "auth_strict_key": False,
            "ssh_config_file": True,
            "channel_log": True,
            "platform": "huawei_olt",
            "timeout_ops": 65,
            "timeout_transport": 65,
            "timeout_socket": 65,
        }
        self.full_ont = []
        self.connect = None
        self.connect_scrapli()

    def connect_scrapli(self):
        try:
            self.connect = Scrapli(**self.OLT)
            self.connect.open()
            for korpus in '3','4','8','10':
                    info = self.connect.send_command("display ont info by-desc SIG-A-K"+korpus).result
                    parse = re.findall(r"^\s+(0)/\s+?([0-9])/(\d+)\s+([0-9]?[0-9])\s+(SIG-A-\S+)", info,re.M)
                    self.full_ont.extend(parse)

        except Exception as E:
            print(f"Error connecting to OLT: {E}")


    def connect_gpon_ont(self):
        ont_rez_dict = {}
        try:
            for i in self.full_ont:
                ont_rez_dict.update({'description': i[-1]})
                ont_info = self.connect.send_command(f'display ont info {" ".join(i[:-1])}').result
                ont_version = self.connect.send_command(f"display ont version {' '.join(i[:-1])}").result
                ont_run = re.search(r"Run state\s+:\s+(\w+)", ont_info, re.M).group(1)
                if ont_run != "offline":
                    math_ip = re.search(r"ONT IP 0 address/mask:\s(\S+)", ont_info, re.M).group(1)
                    ont_rez_dict.update({'ip': math_ip})
                    version = re.search(r"ONT Version \s+:\s+(\S+)",ont_version, re.M).group(1)
                    ont_rez_dict.update({'ont_version': version})
                    equipment_id = re.search(r"Equipment\S+\s+:\s+(\d+)", ont_version, re.M).group(1)
                    ont_rez_dict.update({'equipment_id': equipment_id})
                    m_soft_v = re.search(r"Main Software Version\s+:\s+(\S+)", ont_version,re.M).group(1)
                    ont_rez_dict.update({'main_soft_v': m_soft_v})
                    s_soft_v = re.search(r"Standby Software Version\s+:\s+(\S+)", ont_version,re.M).group(1)
                    ont_rez_dict.update({'standby_soft_v': s_soft_v})
                    print(ont_rez_dict)
                else:
                    print({"description": i[-1], "state":"ONT OFFLINE"})

        except Exception as E:
            print(f"Error retrieving GPON ONT info: {E}")
        finally:
            if self.connect:
                self.connect.close()  #



class ConnectONT:
    def __init__(self, filename):
        try:
            new_list_ont = list()
            full_no_dup = list()
            with open(filename, mode='r', encoding='UTF-8') as f:
                self.data = json.load(f)
                for i in self.data:
                    if i['equipment_id'] != '240' and i['ont_version'] not in new_list_ont:
                        new_list_ont.append(f"{i['ont_version']}")
                        full_no_dup.append(f"{i['description']},{i['ip']}, {i['ont_version']},{i['equipment_id']},{i['main_soft_v']},{i['standby_soft_v']}")
            for i in full_no_dup:
                print(i)


        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Проверьте формат файла.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


class OntConfiguration:
    def __init__(self, *args, **kwargs):
        with open('test.json', mode='r', encoding='UTF-8') as file:
            self.ont = json.load(file)
        self.username = os.getenv("ONT_USERNAME")
        self.password = os.getenv("ONT_PASSWORD")
        self.url = f"{self.ont['ip']}"
        headers = {
            'Host': '10.50.40.124:80',
            # 'Origin': 'https://10.50.40.124:80',
            # 'Connection': 'keep-alive',
            # 'Accept': '*/*',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
            # 'Referer': 'https://10.50.40.124:80/',
            # 'Accept-Language': 'ru',
            # 'X-Requested-With': 'XMLHttpRequest',
        }

        with httpx.Client(verify=False) as session:
            token = session.request(url='https://10.50.40.124:80/asp/GetRandCount.asp', method='POST', timeout=10).text
            print(token)

if __name__ == '__main__':
    ont = OntConfiguration()
