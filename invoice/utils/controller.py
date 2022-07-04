import base64
import requests as re
from .payload import *
from .encrpt import decode, encode
import base64
import gzip

def data_controlller():

    inv_json = json.dumps()
    msg = encode(inv_json).decode("utf-8")
    data_dump = payload_info(request.user.company1.tin, request.user.company1.device_number,ic,msg)
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
        if content:
            decoded = decode(content)
            return_json = json.loads(decoded.decode()) 
        else:
            return_json = None
    except re.HTTPError as ex:
        return "No data got"
    return return_json