# modules/sg_check.py

import boto3
from colorama import Fore, Style

def run():
    print(Fore.CYAN + "[+] Güvenlik grubu (SG) denetimi başlatılıyor..." + Style.RESET_ALL)

    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_groups()
        groups = response.get('SecurityGroups', [])

        if not groups:
            print(Fore.YELLOW + "[!] Hiç güvenlik grubu bulunamadı." + Style.RESET_ALL)
            return

        risky = False

        for group in groups:
            group_name = group.get('GroupName', 'Bilinmeyen')
            group_id = group.get('GroupId', '')
            for permission in group.get('IpPermissions', []):
                from_port = permission.get('FromPort')
                to_port = permission.get('ToPort')
                ip_ranges = permission.get('IpRanges', [])

                for ip_range in ip_ranges:
                    cidr = ip_range.get('CidrIp', '')
                    if cidr == "0.0.0.0/0":
                        risky = True
                        port_info = f"{from_port}-{to_port}" if from_port != to_port else f"{from_port}"
                        print(Fore.RED + f"[!] {group_name} ({group_id}) grubunda {port_info} portu herkese açık!" + Style.RESET_ALL)

        if not risky:
            print(Fore.GREEN + "[+] Tüm güvenlik grupları güvenli. Açık port bulunamadı." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[!] SG taraması sırasında hata oluştu: {e}" + Style.RESET_ALL)
