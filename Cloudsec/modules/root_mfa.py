# modules/root_mfa.py

import boto3
from colorama import Fore, Style

def run():
    print("MFA kontrol başlatılıyor...")  # Kontrol noktası 1

    try:
        iam = boto3.client("iam")
        print("IAM client oluşturuldu.")  # Kontrol noktası 2

        summary = iam.get_account_summary()
        print("get_account_summary() çağrıldı.")  # Kontrol noktası 3

        mfa_enabled = summary['SummaryMap'].get('AccountMFAEnabled', 0)
        print("MFA Enabled:", mfa_enabled)  # Kontrol noktası 4

        if mfa_enabled == 1:
            print(Fore.GREEN + "[✓] Root kullanıcıda MFA AKTİF." + Style.RESET_ALL)
        else:
            print(Fore.RED + "[!] Root kullanıcıda MFA AKTİF DEĞİL!" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"HATA: {e}" + Style.RESET_ALL)  # En önemli kısım
