import base64
import requests as re
from .payload import *
from .encrpt import decode, encode
import base64
import gzip

base_url = "http://198.58.118.119:9880/efristcs/ws/tcsapp/getInformation"

def post_message(data_dump):
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
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


def systemDict(tin, device_no):
    ic = "T115"
    message = ""
    data_dump = payload_info(tin, device_no,ic,message)
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
        gz = base64.b64decode(content)
        ggz = gzip.decompress(gz).decode('UTF8')

        to_bytes = content.encode('utf-8')
        pw = to_bytes.decode("utf-8")
        return content
    except re.HTTPError as ex:
        return "No data got"
    # return response_data

def goodsUpload(tin, device_no, message):
    ic = "T130"
    encode_message = encode(str([message])).decode()
    data_dump = payload_info(tin, device_no, ic, encode_message)
    response_data = post_creditnote(data_dump)
    return response_data


def uploadInvoice(issuer, context,goodsDetails, taxDetails,summary_json):
    interface_code = "T109"
    message = invoice_load(issuer, context, goodsDetails, taxDetails,summary_json)
    to_json = json.dumps(message)
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
        return "No data received back"

def post_creditnote(data_dump):
    try:
        r = re.post(base_url, json=data_dump)
        print(r.json())
        content = r.json()['data']['content']
        decoded = decode(content)
        return r.json()
    except re.HTTPError as ex:
        return "No data got"

def creditNoteUpload(message, request):
    ic = "T110"
    data_dump = payload_info(request.user.company1.tin, request.user.company1.device_number,ic,message)
    response_data = post_creditnote(data_dump)
    return response_data

def refreshCnStatus(tin, numb, msg):
    ic = "T112"
    data_dump = payload_info(tin, numb,ic,msg)
    r = re.post(base_url, json=data_dump)
    content = r.json()['returnStateInfo']['returnMessage']
    return content

def cnListUpload(msg, request):
    ic = "T111"
    data_dump = payload_info(request.user.company1.tin, request.user.company1.device_number,ic,msg)
    return_msg = post_message(data_dump)
    return return_msg


def invListUpload(start_date, end_date, request):
    json_req = {
        "invoiceKind": "1",
        "pageNo": "1",
        "pageSize": "99",
        "startDate": start_date,
        "endDate": end_date,
    }

    ic = "T106"
    inv_json = json.dumps(json_req)
    msg = encode(inv_json).decode("utf-8")
    data_dump = payload_info(request.user.company1.tin, request.user.company1.device_number,ic,msg)
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
        try:
            decoded = decode(content)
            return_json = json.loads(decoded.decode()  ) 
        except:
            gz = base64.b64decode(content)
            return_json = json.loads(gzip.decompress(gz).decode('UTF8'))
            
    except re.HTTPError as ex:
        return "No data received back"
    return return_json

def msg_middleware(request, msg):
    json_req = {
        "invoiceNo": msg
        }

    ic = "T108"
    inv_json = json.dumps(json_req)
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

def cancel_cn_helper(request, msg):
    json_req = {
        "oriInvoiceId": "31000000000000000001",
        "invoiceNo": "786059685752403327",
        "reason": "reason",
        "reasonCode": "102",
        "invoiceApplyCategoryCode": "104"
    }

    ic = "T114"
    inv_json = json.dumps(json_req)
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