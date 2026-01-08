import boto3
from botocore.exceptions import ClientError

def run():
    print("[*] CloudTrail denetimi başlatıldı")

    client = boto3.client("cloudtrail")

    try:
        trails = client.describe_trails()["trailList"]

        if not trails:
            print("[CRITICAL] CloudTrail bulunamadı! Logging yok.")
            return

        for trail in trails:
            name = trail.get("Name")
            is_multi = trail.get("IsMultiRegionTrail")
            s3_bucket = trail.get("S3BucketName")

            status = client.get_trail_status(Name=name)
            is_logging = status.get("IsLogging")

            print(f"\nTrail Name: {name}")

            if not is_logging:
                print("[HIGH] Logging aktif değil")
            else:
                print("[OK] Logging aktif")

            if not is_multi:
                print("[MEDIUM] Multi-region trail değil")
            else:
                print("[OK] Multi-region aktif")

            if not s3_bucket:
                print("[HIGH] Loglar S3'e yazılmıyor")
            else:
                print(f"[OK] Log S3 Bucket: {s3_bucket}")

    except ClientError as e:
        print(f"[ERROR] CloudTrail erişim hatası: {e}")
