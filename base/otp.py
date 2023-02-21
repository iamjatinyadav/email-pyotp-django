import pyotp
import base64


def generate_otp(user):

    # abcd = pyotp.random_base32(100)
    # print(abcd)
    token = base64.b32encode(user.encode())
    otp = pyotp.TOTP(token, interval=600)
    print(token, otp.now())
    return {'secret': token, 'OTP': otp.now()}
