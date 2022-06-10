
import json


def goods_details(prod, number):
    goods ={
            "item": str(prod.product.name),
            "itemCode": str(prod.product.code),
            "qty": str("{:.2f}".format(prod.quantity)),
            "unitOfMeasure": str(prod.product.unit_measure.code),
            "unitPrice": "{:.2f}".format(prod.price),
            "total": str("{:.2f}".format(prod.total())),
            "taxRate": str(0.18) if prod.product.tax_rate =="18%" else str(0),
            "tax": "{:.2f}".format(prod.tax()),
            "discountTotal": "",
            "discountTaxRate": "",
            "orderNumber": str(number),
            "discountFlag": "2",
            "deemedFlag": "2",
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

def tax_details(tax):
    tax = {
            "taxCategory": "A: VAT-Standard",
            "taxCategoryCode":"01",
            "netAmount": "{:.2f}".format(tax.net_amount()),
            "taxRate": str(0.18) if tax.product.tax_rate =="18%" else str(0),
            "taxAmount": str("{:.2f}".format(tax.tax())),
            "grossAmount": str(tax.total()),
            "exciseUnit": "",
            "exciseCurrency": "",
            "taxRateName": "Standard"
        }
    return tax

def summary(summary_details):
    inv_summary = {
            "netAmount": str("{:.2f}".format(summary_details['net'])),
            "taxAmount": str("{:.2f}".format(summary_details['tax'])),
            "grossAmount": str("{:.2f}".format(summary_details['gross'])),
            "itemCount": str(summary_details['itemCount']),
            "modeCode": "1",
            "remarks": str(summary_details['remarks']),
            "qrCode": ""
        }
    return inv_summary