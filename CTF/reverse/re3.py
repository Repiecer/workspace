import base64

encoded = "V1NDVEZ7UzFuQGxfaXNfc29fZUBzeX0="
decoded = base64.b64decode(encoded)
print("解码结果:", decoded.decode())


