from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from alipay import AliPay
from alipay.utils import AliPayConfig
import time

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/retrievalsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Set to a secure random key

# Initialize the database object
db_init = SQLAlchemy(app)

# Initialize JWT
jwt = JWTManager(app)

# Alipay configuration
ALIPAY_APP_ID = '9021000140646310'
ALIPAY_APP_PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
MIIEowIBAAKCAQEAoqSTRY6DG2PO+Tpcsz+mbSVWcAIeJfNDu0sVaLV74pbxRGId
DppCQiMr6tmY8pE8/FP4BRufLHCPPwQxD1p0JDFKzbzSL8ZS1lXoAwLTi9JFc//T9
zL5maWjs+CV6HDffi3onzbpIG2vPvSJdWjFvIM3YOnav1+PATWz3mlzCDqmXdEXe
ZEt79eXuPOS73P5xRoHC+R0zRs/oPdXscXm/+1BHJSTokEVn/pdLUySkYjwpyVSx
RaU8G9Ushu0eqoKMf/L74Dcvq9OyPUU6ciyL5ixft1bFzNKw0aAhfEzM7zKC7+qUp
K/tClCcVVxKVaJb7VTPq05RPpduxBzPaYUoQIDAQABAoIBAAQGeraf/lKxN7AnZ5/
wFVhiMi93ffOGf8ik5RTAWR6UicgdfYac/sLQSAf59rUaLx43nc3Sjy/0YTc4DVbJ
8FHs/mL1J2aTS/2OBr38VewB+kIStNZLZq4M0W5kQpGMKZvf2wAFxeNNk6bFOpmzT
CGMRdSaNRXDcbCf+aGpjnVHpDV8i+YsQuo/odxzSPNStyF0yjzGH1BoY4NkMAJ2lK
oI54Vz3pOiVsvZCsJhC2T0dedQAz0Z6cNBfBYodIO4gEQkrsbB0fjWi3lX633DXCS
1SQrs8oCKwvOWros/NgRHG8dnE4wt9I+z2rjUWiW00Znmyo4TcWzD++iAkOFpsAEC
gYEA1o3l8QzBJyKSVfYFUKYtdhiZjPbu2S0kYMuopclkrHI/sK5R+WSet1GI1L1DB
lWoS5tyQUTax20WPt+gSftWENl7gahesmo58bGYAs/OHYVasZCNkVe3WZdMmImbwn
EXRx/PGPAfcgqo7HCIX9Y04sf+Lnj8yNF8o95Jm2GzycECgYEAwg+QBXufjxYZ/oN
NXffjU1nPwX1iz/DR82LFKXCmz8NogTkChNqwMIGbGq3wA953FDGXhNtHB7nCno8p
PQO+q0awpyuTsBDTYYcz5zjHdWdpmZ+2yJDh+ubnk7c+Mqf0Ggq9R/QMSAjD0fMO4
undQxvQ9KezrLWOqlF++GAeQuECgYAdm69juHLfR7ISEsVg/82+Ql7OSTVk2wnuIa
zAVC6Eba/EXgoJ9IzCl4necc/SC/gRlv4Ja8sVQkSToKCqFPknkhutJOMMlAQzCmM
D4FF9WW3OmzguGoC+6FY1pqfMCXdA5W7a7igowLfXCSCIuTLLKPY2y5N20xH0OzTF
MJJzAQKBgFzo+Io3etgVu9JH6PWxZgwU9svrjTCDWvGM+1pwzdyw8MrVkagrz6kZl
Dn8xuoDS73GVIXOOj6vqEcjwZmtvk7gZFlVGrt0AtAx3B6653wFS+C6P9fczeTDQm
JNnCDCmrMRKzhU1sByOda96QWo9D9aBPvtgq+QqUJQDFs8IaDhAoGBAKeeKJ88FbD
mcF6SK/Vi+zNzCvaj2IfEUAUEfEqMi+QacQwunm+CezKXREricSc2XMVSBbZAaSan
X6i4WVbUJkiavkLCM8IUu7gRbHbQkYGuQWneJp/78mn7kxx870kVOC8ZEJMI6YZXe
xBt6rfkdlqLqlFB0zjMsZwYTjtdr4Xs
-----END PRIVATE KEY-----'''

ALIPAY_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo3/FRq6TpDSiU2g5/v38
g9Sv4Kq2wJ6/DIE7x1sbqdqFJdYFSYTd4b5lCGs/zBsuK70cBD/YsofhnN+1UOF6I
u8m37ldENKdNX8Pnq2wDgv74eFuh4GvvmI0g96iG5vPCJ0vQB53tpdkRgm/BeOsYt
6NTDrWjferwfqL1nyJPCl3b0Y3bgEubo0ncrUOY5g/jNOWOWVMClO4AAy3WKG4qx9
td9Q5gQjFxNg0Bk7reW1xpT5APNf+5muLlylyRC2jfOimj3g3v1GnFgXtP8vKwyIp
2uctFvLzANHD32KzTRzficgGebWnxe/24oBJPbNVKe8vNfP9CSWDQ3JSPQaF1wIDA
QAB
-----END PUBLIC KEY-----'''

# Configure Alipay client
alipay = AliPay(
    appid=ALIPAY_APP_ID,
    app_notify_url=None,  # 默认回调 URL
    app_private_key_string=ALIPAY_APP_PRIVATE_KEY,
    alipay_public_key_string=ALIPAY_PUBLIC_KEY,
    sign_type="RSA2",  # 使用 RSA2 更安全
    debug=True,  # 如果你在沙箱环境下测试，请设置为 True
    config=AliPayConfig(timeout=15)
)
