from datetime import datetime
import json
import pytz
from .encrpt import encode

now = datetime.now()
dt_string = datetime.now(pytz.timezone('Africa/Nairobi')
                         ).strftime("%Y-%m-%d %H:%M:%S")

date_string = datetime.now(pytz.timezone('Africa/Nairobi')
                         ).strftime("%Y-%m-%d")
def payload_info(request, ic, message):
    dt_string = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %H:%M:%S")

    load = {
        "data": {
            "content": message,
            "signature": "",
            "dataDescription": {
                "codeType": "0",
                "encryptCode": "1",
                "zipCode": "0"
            }
        },
        "globalInfo": {
            "appId": "AP04",
            "version": "1.1.20191201",
            "dataExchangeId": "9230489223014123",
            "interfaceCode": str(ic),
            "requestCode": "TP",
            "requestTime": str(dt_string),
            "responseCode": "TA",
            "userName": "admin",
            "deviceMAC": "FFFFFFFFFFFF",
            "deviceNo": str(request.user.company1.device_number),
            "tin": str(request.user.company1.tin),
            "brn": "",
            "taxpayerID": "1",
            "longitude": "116.397128",
            "latitude": "39.916527",
            "extendField": {
                "responseDateFormat": "dd/MM/yyyy",
                "responseTimeFormat": "dd/MM/yyyy HH:mm:ss"
            }
        },
        "returnStateInfo": {
            "returnCode": "",
            "returnMessage": ""
        }
    }
    
    return load

def invoice_load(request, context, goodsDetails, taxDetails,summary_json, payment_details):
    message = {
        "sellerDetails": {
            "tin": str(request.user.company1.tin),
            "ninBrn": "",
            "legalName": str(request.user.company1.name),
            "businessName": "",
            "address": "",
            "mobilePhone": "",
            "linePhone": "",
            "emailAddress": request.user.company1.email,
            "placeOfBusiness": "",
            "referenceNo": context["invoice"].inv_number(),
        },
        "basicInformation": {
            "invoiceNo": "",
            "antifakeCode": "",
            "deviceNo": str(request.user.company1.device_number),
            "issuedDate": str(dt_string),
            "operator": context["operator"],
            "currency": context["currency"],
            "oriInvoiceId": "",
            "invoiceType": "1",
            "invoiceKind": "1",
            "dataSource": "106",
            "invoiceIndustryCode": context["industryCode"][0],
            "isBatch": "0"
        },
        "buyerDetails": {
            "buyerTin": str(context["buyerTin"]),
            "buyerNinBrn": "",
            "buyerPassportNum": "",
            "buyerLegalName": context["buyerLegalName"][0],
            "buyerBusinessName":context["buyerLegalName"][0],
            "buyerAddress": "",
            "buyerEmail": context['buyerEmail'][0],
            "buyerMobilePhone": "",
            "buyerLinePhone": "",
            "buyerPlaceOfBusi": "",
            "buyerType": str(context['buyerType']),
            "buyerCitizenship": "",
            "buyerSector": "",
            "buyerReferenceNo": ""
        },
        "goodsDetails": goodsDetails,
        "taxDetails": taxDetails,
        "summary": summary_json,
        "payWay": payment_details,
        "extend": {
            "reason": "",
            "reasonCode": ""
        }
    }
    return message


def stockGoods(data):
    stockIn = {
        "goodsStockIn": {
            "operationType": "101",
            "remarks": "",
            "stockInDate": date_string,
            "stockInType": "103",
            "productionBatchNo": "3",
            "productionDate": date_string,
            "branchId": ""
        },
        "goodsStockInItem": [
            {
                "goodsCode": str(data['code']),
                "quantity": str(data['quantity']),
                "unitPrice": str(data['unitPrice'])
            }
        ]
    }
    return stockIn

def cnQueryList(date1, date2, query):
    json_req = {
        "queryType": query,
        "invoiceApplyCategoryCode": "101",
        "startDate": date1,
        "endDate": date2,
        "pageNo": "1",
        "pageSize": "50"
        }
    return json_req