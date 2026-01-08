import boto3
import json
from colorama import Fore, Style

def get_iam_users():
    iam = boto3.client("iam")
    users = []
    response = iam.list_users()
    for user in response['Users']:
        users.append(user['UserName'])
    return users

def get_attached_policies(user):
    iam = boto3.client("iam")
    attached = iam.list_attached_user_policies(UserName=user)
    return [p['PolicyArn'] for p in attached['AttachedPolicies']]

def get_inline_policies(user):
    iam = boto3.client("iam")
    inline_names = iam.list_user_policies(UserName=user)['PolicyNames']
    docs = []
    for name in inline_names:
        doc = iam.get_user_policy(UserName=user, PolicyName=name)
        docs.append(doc['PolicyDocument'])
    return docs

def get_policy_doc(arn):
    iam = boto3.client("iam")
    policy = iam.get_policy(PolicyArn=arn)
    version = policy['Policy']['DefaultVersionId']
    doc = iam.get_policy_version(PolicyArn=arn, VersionId=version)
    return doc['PolicyVersion']['Document']

def find_risky_actions(policy_doc):
    risky = ['iam:*', '*:*', 'iam:PassRole', 'iam:CreateAccessKey', 'iam:PutUserPolicy']
    found = []
    statements = policy_doc.get('Statement', [])
    if isinstance(statements, dict):  
        statements = [statements]
    for stmt in statements:
        actions = stmt.get('Action', [])
        if isinstance(actions, str):
            actions = [actions]
        for action in actions:
            for risk in risky:
                if action == risk or (risk.endswith('*') and action.startswith(risk[:-1])):
                    found.append(action)
    return list(set(found))

def run():
    print(Fore.CYAN + "[+] IAM kullanıcı analizi başlatılıyor...\n" + Style.RESET_ALL)
    users = get_iam_users()
    results = {}

    for user in users:
        all_policies = []

        # attached
        for arn in get_attached_policies(user):
            doc = get_policy_doc(arn)
            all_policies.append(doc)

        # inline
        all_policies += get_inline_policies(user)

        # riskleri bul
        risky = []
        for doc in all_policies:
            risky += find_risky_actions(doc)

        if risky:
            print(Fore.RED + f"[!] Riskli kullanıcı: {user} → {risky}" + Style.RESET_ALL)
            results[user] = list(set(risky))
        else:
            print(Fore.GREEN + f"[+] {user} kullanıcısında riskli izin yok." + Style.RESET_ALL)

   #json kaydet
    with open("iam_report.json", "w") as f:
        json.dump(results, f, indent=4)

    print(Fore.CYAN + "\n[+] IAM kontrolü tamamlandı. Rapor: iam_report.json\n" + Style.RESET_ALL)
