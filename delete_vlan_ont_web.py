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
        self.connect_gpon_ont()

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
        try:
            ont_rez_dict = {}
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
            json_object = json.dumps(ont_rez_dict, indent=4)

            with open("ont_data.json", "w") as outfile:
                outfile.write(json_object)
        except Exception as E:
            print(f"Error retrieving GPON ONT info: {E}")
        finally:
            if self.connect:
                self.connect.close()  #


if __name__ == '__main__':
    ont = ConnectOLT()
