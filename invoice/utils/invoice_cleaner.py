from datetime import datetime
import json
from .encrpt import *

def inv_context(input):
    to_json = json.loads(input)
    output = {}
    output['antifake'] = to_json['basicInformation']['antifakeCode']
    output['deviceNo'] = to_json['basicInformation']['deviceNo']
    output['invoiceId'] = to_json['basicInformation']['invoiceId']
    output['currency'] = to_json['basicInformation']['currency']
    output['fdn'] = to_json['basicInformation']['invoiceNo']

    if '-' in to_json['basicInformation']['issuedDate']:
        output['date'] = datetime.strptime(to_json['basicInformation']['issuedDate'],'%Y-%m-%d %H:%M:%S')
    else:
        output['date'] = datetime.strptime(to_json['basicInformation']['issuedDate'],'%d/%m/%Y %H:%M:%S')
        
    output['qrcode'] = to_json['summary']['qrCode']
    output['gross'] = float(to_json['summary']['grossAmount'])
    output['net'] = float(to_json['summary']['netAmount'])
    output['itemNo'] = to_json['summary']['itemCount']
    output['tax'] = float(to_json['summary']['taxAmount'])
    output['buyerName'] = to_json['buyerDetails']['buyerBusinessName']
    output['invoice_number'] = to_json['sellerDetails']['referenceNo']
    try:
        if to_json['buyerDetails']['buyerTin']:
            output['buyerTin'] = to_json['buyerDetails']['buyerTin']
        else:
            output['buyerTin'] = ""
    except:
        output['buyerTin'] = ""

    output['items'] = []
    for itm in to_json['goodsDetails']:
        output['items'].append(itm)

    output['taxDetails'] = []
    for item in to_json['taxDetails']:
        output['taxDetails'].append(item)

    return output

def cn_context(jsonrep):
    output = {}
    to_json = json.dumps(jsonrep, indent=4)
    content = to_json['data']['content']
    decoded_json = decode(content)
    # output['antifake'] = to_json['basicInformation']['antifakeCode']
    # output['deviceNo'] = to_json['basicInformation']['deviceNo']
    # output['invoiceId'] = to_json['basicInformation']['invoiceId']
    # output['currency'] = to_json['basicInformation']['currency']

    # output['fdn'] = to_json['basicInformation']['invoiceNo']
    # output['date'] = datetime.strptime(to_json['basicInformation']['issuedDate'], '%d/%m/%Y %H:%M:%S')
    # output['qrcode'] = to_json['summary']['qrCode']
    # output['gross'] = float(to_json['summary']['grossAmount'])
    # output['net'] = float(to_json['summary']['netAmount'])
    # output['itemNo'] = to_json['summary']['itemCount']
    # output['tax'] = float(to_json['summary']['taxAmount'])
    # output['buyerName'] = to_json['buyerDetails']['buyerBusinessName']
    # output['buyerTin'] = to_json['buyerDetails']['buyerTin']
    return output