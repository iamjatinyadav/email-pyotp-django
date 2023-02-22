import pyotp
import base64
from .email import *


def generate_otp(user):
    token = base64.b32encode(user.encode())
    otp = pyotp.TOTP(token, interval=600)
    send_otp_via_mail(user, otp.now())


def generate_verify_otp(user):
    token = base64.b32encode(user.encode())
    otp = pyotp.TOTP(token, interval=600)
    return {'token': token, 'OTP': otp.now()}
