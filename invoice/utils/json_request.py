

def cn_approval_request(msg):
    ic = 'T113'
    json_req = {
        "referenceNo": msg['ref'],
        "approveStatus": "101",
        "taskId": "1",
        "remark": msg['remarks']
        }
    return json_req