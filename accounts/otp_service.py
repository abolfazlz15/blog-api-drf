import random
import string
from django.core.cache import cache
import datetime


class OTP:

    def __init__(self):
        self.otp_expiry_minutes = 2

    def generate_otp(self, email):
        otp = ''.join([random.choice(string.digits) for n in range(6)])
        cache.set(email, otp, self.otp_expiry_minutes * 60)
        print(otp)
        return otp

    def verify_otp(self, otp, email):
        stored_otp = cache.get(email)
        if stored_otp == otp:
            return True
        else:
            return False

    def clear_otp(self, email):
        cache.delete(email)

    def send_otp(self, otp, email):
        # Send OTP to the email address

        pass
