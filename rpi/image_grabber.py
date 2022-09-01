import time
import os
import optparse

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# 3rd party
from picamera import PiCamera
import boto3
import boto_patch

# Yubico
import yubihsm.exceptions
from yubihsm import YubiHsm
from yubihsm.objects import WrapKey


def parse_options():
    usage = """\
    rpi_image_grabber.py [options...]
    This script will startup the image grabber service."""
    parser = optparse.OptionParser(usage=usage)

    parser.add_option(
        "-i",
        "--hsmipport",
        dest="hsmipport",
        default='',
        help="IP:Port for the YubiHSM",
    )
    
    parser.add_option(
        "-u",
        "--userid",
        dest="userid",
        default='',
        help="What userid for the YubiHSM",
    )

    parser.add_option(
        "-p",
        "--userpass",
        dest="userpass",
        default='',
        help="Password for the YubiHSM user",
    )

    parser.add_option(
        "-w",
        "--wrapid",
        dest="wrapid",
        default='',
        help="Wrap ID on the YubiHSM",
    )

    parser.add_option(
        "-b",
        "--bucketname",
        dest="bucketname",
        default='',
        help="Bucket name in AWS",
    )

    parser.add_option(
        "-l",
        "--localpath",
        dest="localpath",
        default='',
        help="Local path to store files",
    )

    options, _ = parser.parse_args()
    # All options are required
    return options


def dataupload(filename, configs):

    # HSM information
    hsmipport = configs.hsmipport
    userid = int(configs.userid)
    userpass = configs.userpass

    # What wrap key to use
    wrapid = int(configs.wrapid)

    # Files
    path = configs.localpath
    bucketname = configs.bucketname

    try:
        hsm = YubiHsm.connect(f"http://{hsmipport}")
        session = hsm.create_session_derived(userid, userpass)

        # Get random data from YubiHSM
        key = session.get_pseudo_random(32)
        iv = session.get_pseudo_random(16)

        # Encrypt the key used for encryption
        enckey = WrapKey(session=session, object_id=wrapid).wrap_data(key)

        # Initialize AES object
        aes = AES.new(key, AES.MODE_CBC, iv)

        with open(f"{path}/{filename}.enc", 'wb') as fileout:
            hiv = iv.hex()
            henckey = enckey.hex()
            fileinst = f"{hiv}||{henckey}||".ljust(200, '0')
            fileout.write(fileinst.encode())

            with open(f"{path}/{filename}", 'rb') as filein:
                filecont = filein.read()
                encdata = aes.encrypt(pad(filecont, AES.block_size))
                fileout.write(encdata)

        # Upload to AWS
        s3_client = boto3.client('s3')
        s3_client.upload_file(f"{path}/{filename}.enc", bucketname, f"{filename}.enc")
    except Exception as err:
        os.remove(f"{path}/{filename}.enc")
        print("Error on upload " + err.__str__())


def space_avail():
    fs = os.statvfs(".")
    mbfree = (fs.f_frsize * fs.f_bfree) * 0.000001

    if mbfree < 10000:
        return False
    return True


def grab_photo(camera, filepath):
    phototime = int(time.time())
    filename = f"photo-{phototime}.jpg"
    fullfilename = f"{filepath}/{filename}"
    camera.annotate_text = f"Captured at: {phototime}"
    camera.exif_tags['IFD0.Copyright'] = 'TreborTech, LLC - HSM Central Management'
    camera.exif_tags['EXIF.UserComment'] = 'Demo unit on 3d printer'
    camera.capture(fullfilename)
    return filename


def router(options):
    camera = PiCamera()
    camera.resolution = (1024, 768)
    filepath = options.localpath
    while True:
        if not space_avail():
            return False
        filename = grab_photo(camera, filepath)
        dataupload(filename, options)
        time.sleep(60)


if __name__ == "__main__":
    options = parse_options()
    router(options)