from webconfig import *
import json

def main():
    file = json.load(open('razobratsa.json', mode='r', encoding='utf-8'))
    try:
        for ont in file:
            if ont.get('main_soft_v') == "V3R016C10S135" or ont.get('main_soft_v') == "V3R016C10S150":
                ONTVersion494EV3R016C10S150(ont.get('ip'))
            elif ont.get('main_soft_v') == 'V1R006C00S122' and ont.get("equipment_id") != '240':
                ONTVersion130DC600(ont.get('ip'))
            elif ont.get('main_soft_v') == 'V1R006C00S210' and ont.get("equipment_id") != '240':
                ONTVersion130AC422(ont.get('ip'))
            elif ont.get('main_soft_v') == 'V1R006C00S200':
                pass
            else:
                print(ont.get('ont_version'),ont.get('main_soft_v'),ont.get('ip'))
    except Exception as E:
        print("Exceptions",ont.get('ont_version'),ont.get('main_soft_v'),ont.get('ip'))
        print(E)




if __name__ == '__main__':
    main()