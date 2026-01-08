# CloudSec Risk Scanner

CloudSec Risk Scanner, AWS ortamlarında yaygın olarak karşılaşılan güvenlik
yanlış yapılandırmalarını tespit etmek amacıyla geliştirilmiş Python tabanlı bir komut satırı (CLI) güvenlik denetim aracıdır.

Proje, bulut ortamlarında hem önleyici güvenlik kontrollerini hem de
olayların tespit edilebilirliğini değerlendirmeyi hedefler.

## Özellikler

- IAM kullanıcı ve yetki denetimi
- Root hesap MFA kontrolü
- Public S3 bucket taraması
- Güvenlik grubu (Security Group) açık port analizi
- CloudTrail logging ve tespit kontrolü

## Proje Yapısı

.
├── cloudscan.py
├── modules/
│ ├── iam_check.py
│ ├── root_mfa.py
│ ├── s3_check.py
│ ├── sg_check.py
│ └── cloudtrail_check.py
├── requirements.txt
└── README.md

## Kurulum

Gerekli Python kütüphanelerini yüklemek için:

```bash
pip install -r requirements.txt
AWS kimlik bilgilerini yapılandırmak için:
aws configure

## Kullanım

Belirli bir denetimi çalıştırmak için:

python cloudscan.py --check iam
python cloudscan.py --check root-mfa
python cloudscan.py --check s3
python cloudscan.py --check sg
python cloudscan.py --check cloudtrail

Tüm denetimleri birlikte çalıştırmak için:
python cloudscan.py --check all

## Güvenlik Yaklaşımı

CloudSec Risk Scanner yalnızca potansiyel güvenlik risklerini tespit etmeyi
değil, aynı zamanda AWS ortamlarında olayların izlenebilir ve analiz edilebilir olup olmadığını da değerlendirmektedir.

CloudTrail denetimi sayesinde, güvenlik olaylarının geriye dönük olarak
incelenebilmesi için gerekli loglama mekanizmalarının durumu kontrol edilir.
