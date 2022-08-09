import base64
import requests as re
from .payload import *
from .encrpt import decode, encode
import base64
import gzip
from django.contrib import messages

def post_message(request, data_dump):
    try:
        r = re.post(request.user.company1.url, json=data_dump)
        content = r.json()['data']['content']
        if r.json()['data']['dataDescription']['zipCode'] == '1':
            gz = base64.b64decode(content)
            return gzip.decompress(gz).decode('utf-8')
        else:
            decoded = decode(content)
            return decoded.decode()
    except re.HTTPError as ex:
        return "No data got"


def getClientDetails(request, client_tin):
    ic = "T119"
    message = encode(str({"tin": client_tin, "ninBrn": ""})).decode()
    data_dump = payload_info(request, ic, message)
    response_data = post_message(request, data_dump)
    return response_data

def systemDict(request):
    ic = "T115"
    message = ""
    data_dump = payload_info(request,ic,message)
    try:
        r = re.post(request.user.company1.url, json=data_dump)
        content = r.json()['data']['content']
        gz = base64.b64decode(content)
        ggz = gzip.decompress(gz).decode('utf-8')

        to_bytes = content.encode('utf-8')
        pw = to_bytes.decode("utf-8")
        return ggz
    except re.HTTPError as ex:
        return "No data got"

def goodsUpload(request, message):
    ic = "T130"
    encode_message = encode(str([message])).decode()
    data_dump = payload_info(request, ic, encode_message)
    response_data = post_creditnote(request, data_dump)
    return response_data

def goodsInquire(request, req):
    ic = 'T127'
    dump = json.dumps(req)
    encode_request = encode(dump).decode()
    outer_json = payload_info(request ,ic,encode_request)
    return post_message(request, outer_json)
    
def uploadInvoice(request, context, goodsDetails, taxDetails,summary_json, payment_detials):
    interface_code = "T109"
    message = invoice_load(request, context, goodsDetails, taxDetails,summary_json, payment_detials)
    to_json = json.dumps(message)
    encode_message = encode(to_json).decode()
    data_dump = payload_info(request, interface_code, encode_message)
    response_data = InvoiceService(request, data_dump)
    return response_data

def InvoiceService(request, data_dump):
    return_info = {}
    try:
        r = re.post(request.user.company1.url, json=data_dump)
        
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

def post_creditnote(request, data_dump):
    base_url = request.user.company1.url
    try:
        r = re.post(base_url, json=data_dump)
        content = r.json()['data']['content']
        return r.json()
    except re.HTTPError as ex:
        return "No data got"

def creditNoteUpload(message, request):
    ic = "T110"
    data_dump = payload_info(request, ic, message)
    response_data = post_creditnote(request, data_dump)
    return response_data

def refreshCnStatus(request, msg):
    ic = "T112"
    data_dump = payload_info(request, ic, msg)
    print(data_dump)
    r = re.post(request.user.company1.url, json=data_dump)
    print(r.json())
    content = r.json()['returnStateInfo']['returnMessage']
    return content

def cnListUpload(msg, request):
    ic = "T111"
    data_dump = payload_info(request, ic, msg)
    return_msg = post_message(request,data_dump)
    
    return return_msg

def invListUpload(start_date, end_date, request):
    json_req = {
        'invoiceType': "2",
        "invoiceKind": "1",
        "pageNo": "1",
        "pageSize": "99",
        "startDate": start_date,
        "endDate": end_date,
    }

    ic = "T106"
    inv_json = json.dumps(json_req)
    msg = encode(inv_json).decode("utf-8")
    data_dump = payload_info(request,ic,msg)
    try:
        r = re.post(request.user.company1.url, json=data_dump)
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
    data_dump = payload_info(request,ic,msg)
    try:
        r = re.post(request.user.company1.url, json=data_dump)
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
        "oriInvoiceId": msg['inv_id'],
        "invoiceNo": msg['cn_ref'],
        "reason": "",
        "reasonCode": msg['reason'],
        "invoiceApplyCategoryCode": "104"
    }

    ic = "T114"
    inv_json = json.dumps(json_req)
    msg = encode(inv_json).decode("utf-8")
    data_dump = payload_info(request,ic,msg)
    try:
        r = re.post(request.user.company1.url, json=data_dump)
        content = r.json()['data']['content']
        print(r.json())
        if content:
            decoded = decode(content)
            return_json = json.loads(decoded.decode()) 
            messages.success(request, return_json['returnStateInfo']['returnMessage'])
        else:
            return_json = None
    except re.HTTPError as ex:
        return "No data got"
    return return_json

def cn_approval_request(msg):
    ic = 'T113'
    json_req = {
        "referenceNo": msg['ref'],
        "approveStatus": "101",
        "taskId": "1",
        "remark": msg['remarks']
        }
    return json_req