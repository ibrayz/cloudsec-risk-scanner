import argparse

from modules import iam_check
from modules import root_mfa
from modules import s3_check
from modules import sg_check
from modules import cloudtrail_check


def main():
    parser = argparse.ArgumentParser(
        description="CloudSec Risk Scanner - AWS Güvenlik Denetim Aracı"
    )

    parser.add_argument(
        "--check",
        choices=[
            "iam",
            "root-mfa",
            "s3",
            "sg",
            "cloudtrail",
            "all"
        ],
        required=True,
        help="Yapılacak güvenlik kontrolünü seçin"
    )

    args = parser.parse_args()

    if args.check == "iam":
        iam_check.run()

    elif args.check == "root-mfa":
        root_mfa.run()

    elif args.check == "s3":
        s3_check.run()

    elif args.check == "sg":
        sg_check.run()

    elif args.check == "cloudtrail":
        cloudtrail_check.run()

    elif args.check == "all":
        print("\n=== [IAM Kullanıcı Denetimi] ===")
        iam_check.run()

        print("\n=== [Root MFA Denetimi] ===")
        root_mfa.run()

        print("\n=== [S3 Bucket Denetimi] ===")
        s3_check.run()

        print("\n=== [Güvenlik Grubu (Security Group) Denetimi] ===")
        sg_check.run()

        print("\n=== [CloudTrail Logging Denetimi] ===")
        cloudtrail_check.run()


if __name__ == "__main__":
    main()


