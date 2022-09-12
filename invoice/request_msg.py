def goods_inquiry_req(prod):
    msg = {
    "goodsCode": prod,
    "goodsName ": "",
    "commodityCategoryName": "",
    "pageNo": "1",
    "pageSize": "10",
    "branchId": ""
    }
    return msg