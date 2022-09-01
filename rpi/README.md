

# My Tools for RaspberryPI


- Image Grabber


## Image Grabber

### My Installation Information

**Distributor ID:**	Raspbian
**Description:**	Raspbian GNU/Linux 11 (bullseye)
**Release:**	11
**Codename:**	bullseye

Additional file needed
- boto_patch.py


`pip3 list`

```
boto3           1.24.62
botocore        1.27.62
certifi         2020.6.20
cffi            1.15.1
chardet         4.0.0
colorzero       1.1
cryptography    37.0.4
distro          1.5.0
gpiozero        1.6.2
idna            2.10
jmespath        1.0.1
picamera        1.13
pip             20.3.4
pycparser       2.21
pycryptodome    3.15.0
python-apt      2.2.1
python-dateutil 2.8.2
requests        2.25.1
RPi.GPIO        0.7.0
s3transfer      0.6.0
setuptools      52.0.0
six             1.16.0
spidev          3.5
ssh-import-id   5.10
urllib3         1.26.5
wheel           0.34.2
yubihsm         2.1.0
```


**S3 Policy**

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:CreateBucket"
            ],
            "Resource": [
                "arn:aws:s3:::yourbucketname",
                "arn:aws:s3:::yourbucketname/*"
            ]
        }
    ]
}
```


**AWS credentials file**

```
[default]
aws_access_key_id = ASDFGHJKLOIUYTREWQZX
aws_secret_access_key = hsm|127.0.0.1:1111|10|password|25000
region=us-east-1
```


**Startup script**

```
/usr/bin/python3 /home/rbooth/rpi_image_grabber.py -i 127.0.0.1:1111 -u 10 -p password -w 15000 -b mys3bucketname -l /photos
```


