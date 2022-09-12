import base64

def encode(text):
    to_bytes = text.encode('utf-8')
    # 'utf-8' ascii
    return (base64.b64encode(to_bytes))

def decode(text):
    return (base64.b64decode(text))