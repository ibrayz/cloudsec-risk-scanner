# modules/s3_check.py

import boto3
from colorama import Fore, Style

def run():
    print(Fore.CYAN + "[+] S3 bucket taraması başlatıldı..." + Style.RESET_ALL)

    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        if not buckets:
            print(Fore.YELLOW + "[!] Hesapta hiç bucket yok." + Style.RESET_ALL)
            return

        risk_found = False

        for bucket in buckets:
            name = bucket['Name']
            print(f"\n[*] İncelenen bucket: {name}")

            # 1. Bucket ACL kontrolü
            try:
                acl = s3.get_bucket_acl(Bucket=name)
                for grant in acl['Grants']:
                    grantee = grant.get('Grantee', {})
                    uri = grantee.get('URI', '')
                    if "AllUsers" in uri or "AuthenticatedUsers" in uri:
                        print(Fore.RED + f"[!] BUCKET herkese açık: {name} (bucket ACL)" + Style.RESET_ALL)
                        risk_found = True
            except Exception as e:
                print(Fore.YELLOW + f"[!] {name} bucket ACL okunamadı: {e}" + Style.RESET_ALL)

            # 2. İçerikteki dosya ACL kontrolü
            try:
                objs = s3.list_objects_v2(Bucket=name).get('Contents', [])
                for obj in objs:
                    key = obj['Key']
                    try:
                        obj_acl = s3.get_object_acl(Bucket=name, Key=key)
                        for grant in obj_acl['Grants']:
                            grantee = grant.get('Grantee', {})
                            uri = grantee.get('URI', '')
                            if "AllUsers" in uri or "AuthenticatedUsers" in uri:
                                print(Fore.RED + f"[!] Public dosya: {name}/{key} → ACL: {uri}" + Style.RESET_ALL)
                                risk_found = True
                    except Exception as e:
                        print(Fore.YELLOW + f"[!] {key} dosyasının ACL'si okunamadı: {e}" + Style.RESET_ALL)

            except Exception as e:
                print(Fore.YELLOW + f"[!] {name} bucket objeleri listelenemedi: {e}" + Style.RESET_ALL)

        if not risk_found:
            print(Fore.GREEN + "[+] Tüm bucket'lar güvenli. Public erişim bulunamadı." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[!] S3 taraması sırasında hata oluştu: {e}" + Style.RESET_ALL)
