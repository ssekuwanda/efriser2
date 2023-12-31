
import json
from platform import python_branch
from invoice.utils.app_utilities import app_time, app_date

def goods_details(prod, number, inv):
    deemed = ''
    deemedFlag = '2'

    if inv.client.company_type == '3':
        deemedFlag = '1'
        deemed = ' '+'(Deemed)'

    tax_rate = ""
    if prod.tax_type.code == "01":
        tax_rate = "0.18"
    elif prod.tax_type.code == "03":
        tax_rate = "-"
    elif prod.tax_type.code == "04":
        tax_rate = "0.18"
    else:
        tax_rate = "0"

    

    goods = {
            "item": str(prod.product.name)+deemed,
            "itemCode": str(prod.product.code),
            "qty": str("{:.2f}".format(prod.quantity)),
            "unitOfMeasure": str(prod.product.unit_measure.code),
            "unitPrice": "{:.2f}".format(prod.price),
            "total": str("{:.2f}".format(prod.total())),
            "taxRate": tax_rate,
            "tax": str(prod.tax()),
            "discountTotal": "",
            "discountTaxRate": "",
            "orderNumber": str(number),
            "discountFlag": "2",
            "deemedFlag": deemedFlag,
            "exciseFlag": "2",
            "categoryId": "",
            "categoryName": "",
            "goodsCategoryId": str(prod.product.commodity_id),
            "goodsCategoryName": str(prod.product.name),
            "exciseRate": "",
            "exciseRule": "",
            "exciseTax": "",
            "pack": "",
            "stick": "",
            "exciseUnit": "",
            "exciseCurrency": "",
            "exciseRateName": ""
        }
    return goods

def tax_details(tax, inv):
    tax_rate = ""
    if tax.tax_type.code == "01":
        tax_rate = "0.18"
    elif tax.tax_type.code == "02":
        tax_rate = "0"
    elif tax.tax_type.code == "03":
        tax_rate = "-"
    else:
        tax_rate = ""

    tax_request = {
            "taxCategoryCode":str(tax.tax_type.code),
            "netAmount": "{:.2f}".format(tax.net_amount()),
            "taxRate": tax_rate,
            "taxAmount": str("{:.2f}".format(tax.tax())),
            "grossAmount": str(tax.total()),
            "exciseUnit": "",
            "exciseCurrency": "",
        }
    return tax_request

def summary(summary_details):
    inv_summary = {
            "netAmount": str("{:.2f}".format(summary_details['net'])),
            "taxAmount": str("{:.2f}".format(summary_details['tax_summary'])),
            "grossAmount": str("{:.2f}".format(summary_details['gross'])),
            "itemCount": str(summary_details['itemCount']),
            "modeCode": "1",
            "remarks": str(summary_details['remarks']),
            "qrCode": ""
        }
    return inv_summary 

def invoice_recovery(summary_details):
    inv = {
        "net_amount": summary_details.amount,
        "amount": summary_details.amount,
        "new_creditnote" : summary_details.fees,
        "tax": summary_details.tax_amount,
        "total_reimbusermnents": summary_details.reimbursements,

    }

def pay_way(details):
    payment_details = {
        "paymentMode": details['payment_method'],
        "paymentAmount": str("{:.2f}".format(details['gross'])),
        "orderNumber": "a"
        },
    return payment_details

def credit_note(note, form, cn_number):
    data = cleaned_json(note.json_response)
    note_details = {
        "oriInvoiceId": data['invoice_id'],
        "oriInvoiceNo": data['fdn'],
        "reasonCode": form.cleaned_data['reason_code'],
        "reason": form.cleaned_data['reason'],
        "applicationTime": str(app_time()),
        "invoiceApplyCategoryCode": '101',
        "currency": data['currency'],
        "contactName": "",
        "contactMobileNum":"",
        "contactEmail":"",
        "source":"103",
        "remarks":"",
        "sellersReferenceNo":cn_number,
        "goodsDetails":data['goodsDetails'],
        "taxDetails":data['taxes'],
        "summary":data['summary'],
        "payWay":data['pay_mode'],
    }
    return note_details

def cleaned_json(jsondata):
    data = {}
    data_dict = json.loads(jsondata)
    data['antifake'] = data_dict['basicInformation']['antifakeCode']
    data['currency'] = data_dict['basicInformation']['currency']
    data['invoice_id'] = data_dict['basicInformation']['invoiceId']
    data['fdn'] = data_dict['basicInformation']['invoiceNo']
    data['date'] = data_dict['basicInformation']['issuedDate']
    data['qr'] = data_dict['summary']['qrCode']
    data['taxes'] = data_dict['taxDetails']
    data['summary'] = data_dict['summary']
    data['pay_mode'] = data_dict['payWay']

    # Turning goods details to negative


    def negative_tranformation():
        all_goods = data_dict['goodsDetails']
        new_goods = []
        for goods in all_goods:
            # ----------------------
            qty_parts = float(goods['qty'])
            neg_qty_parts = str(-1*qty_parts)
            goods.update({'qty':neg_qty_parts}) 
            # ---------------------------
            total_parts = float(goods['total'])
            neg_total_parts = str(-1*total_parts)
            goods.update({'total':neg_total_parts}) 
            # ------------------------
            tax_parts = float(goods['tax'])
            neg_tax_parts = str(-1*tax_parts)
            goods.update({'tax':neg_tax_parts}) 
            new_goods.append(goods)                 
        return new_goods

    data['goodsDetails'] = negative_tranformation()


    def negative_tax():
        all_taxes = data_dict['taxDetails']
        new_taxes = []
        for taxes in all_taxes:
            # ----------------------
            netAmount_parts = float(taxes['netAmount'])
            neg_netAmount_parts = str(-1*netAmount_parts)
            taxes.update({'netAmount':neg_netAmount_parts}) 
            # ---------------------------
            amount_parts = float(taxes['taxAmount'])
            neg_amount_parts = str(-1*amount_parts)
            taxes.update({'taxAmount':neg_amount_parts}) 
            # ------------------------
            gross_parts = float(taxes['grossAmount'])
            neg_gross_parts = str(-1*gross_parts)
            taxes.update({'grossAmount':neg_gross_parts}) 
            new_taxes.append(taxes)                 
        return new_taxes
    data['taxDetails'] = negative_tax()


    def negative_summary():
        sum = data_dict['summary']
        # ----------------------
        netAmount_parts = float(sum['netAmount'])
        neg_netAmount_parts = str(-1*netAmount_parts)
        sum.update({'netAmount':neg_netAmount_parts}) 
        # ---------------------------
        amount_parts = float(sum['taxAmount'])
        neg_amount_parts = str(-1*amount_parts)
        sum.update({'taxAmount':neg_amount_parts}) 
        # ------------------------
        gross_parts = float(sum['grossAmount'])
        neg_gross_parts = str(-1*gross_parts)
        sum.update({'grossAmount':neg_gross_parts}) 
        # ----------------------------------
        sum['modeCode'] = "0"
        return sum
    data['summary'] = negative_summary()
    return data


def stockInGoods(goodsDetail):
    stock = {
            "goodsStockIn": {
            "operationType": "101",
            "remarks": "Increase inventory",
            "stockInDate": str(app_date()),
            "stockInType": "103",
            "productionBatchNo": "1200983",
            "productionDate": str(app_date()),
            "branchId": "",
            },
            "goodsStockInItem": [{
            "commodityGoodsId": goodsDetail['commodityGoodsId'],
            "quantity": goodsDetail['quantity'],
            "unitPrice": goodsDetail['unitPrice'],
            }]
        }
    return stock

