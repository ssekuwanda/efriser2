from ast import Return
from email import message
import requests as re
from .payload import *
from .encrpt import decode, encode

base_url = "http://198.58.118.119:9880/efristcs/ws/tcsapp/getInformation"

def post_message(data_dump):
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
        print(r.json())
        decoded = decode(content)
        return decoded.decode()
    except re.HTTPError as ex:
        return "No data got"

def getClientDetails(tin, client_tin, device_no):
    ic = "T119"
    message = encode(str({"tin": client_tin, "ninBrn": ""})).decode()
    data_dump = payload_info(tin, device_no,ic,message)
    response_data = post_message(data_dump)

    return response_data


def goodsUpload(tin, device_no, message):
    ic = "T130"
    encode_message = encode(str([message])).decode()
    data_dump = payload_info(tin, device_no, ic, encode_message)
    response_data = post_message(data_dump)
    return response_data


def uploadInvoice(issuer, context,goodsDetails, taxDetails,summary_json):
    interface_code = "T109"

    message = invoice_load(issuer, context, goodsDetails, taxDetails,summary_json)

    to_json = json.dumps(message)
    print(to_json)
    encode_message = encode(to_json).decode()

    tin = issuer.tin
    device_no = issuer.device_number

    data_dump = payload_info(tin, device_no, interface_code, encode_message)
    response_data = InvoiceService(data_dump)

    return response_data


def InvoiceService(data_dump):
    return_info = {}
    try:
        r = re.post(base_url, json=data_dump)
        
        if "returnStateInfo" in r.json():
            return_code = r.json()["returnStateInfo"]
            return_info.update(return_code)
        else:
            return_info['return_code'] = ""

        if "data" in r.json():
            normal_content = r.json()["data"]["content"]
            decoded = decode(normal_content)
            decoded_content = decoded.decode()
            return_info['content'] = decoded_content
        else:
            return_info["content"]=""

        return return_info
    except re.HTTPError as ex:
        return "No data got"

