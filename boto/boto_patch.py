import hashlib
import hmac

from hashlib import sha256

import botocore.auth as BOTOAUTH

import yubihsm.exceptions
from yubihsm import YubiHsm
from yubihsm.objects import HmacKey


def hsm_sign(key, msg):
    # Only the first signing operation needs to access the YubiHSM
    # Key format
    # hsm | hsmip:port | userid | userpassword | hmacid
    # hsm|192.168.1.10|1|password|2
    arrkey = key.split("|")
    hsmipport = arrkey[1]
    authid = int(arrkey[2])
    password = arrkey[3]
    keyid = int(arrkey[4])

    try:
        hsm = YubiHsm.connect(f"http://{hsmipport}/api")
        session = hsm.create_session_derived(authid, password)
    except yubihsm.exceptions.YubiHsmAuthenticationError:
        message = "Login failed"
        return (False, message)
    except yubihsm.exceptions.YubiHsmConnectionError:
        message = "No route to host"
        return (False, message)
    except yubihsm.exceptions.YubiHsmDeviceError:
        message = "Login failed 2"
        return (False, message)
    except yubihsm.exceptions.YubiHsmInvalidResponseError:
        message = "Response error"
        return (False, message)

    sha256hash = sha256()
    sha256hash = msg.encode()

    hmackey = HmacKey(session, keyid)
    return hmackey.sign_hmac(sha256hash)


def hsm_signature(self, string_to_sign, request):
    key = self.credentials.secret_key
    if key[:3] == "hsm":
        k_date = hsm_sign(key, request.context["timestamp"][0:8])
    else:
        k_date = self._sign(
            (f"AWS4{key}").encode(), request.context["timestamp"][0:8]
        )
    k_region = self._sign(k_date, self._region_name)
    k_service = self._sign(k_region, self._service_name)
    k_signing = self._sign(k_service, 'aws4_request')
    return self._sign(k_signing, string_to_sign, hex=True)

BOTOAUTH.SigV4Auth.signature = hsm_signature

