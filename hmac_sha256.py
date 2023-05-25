import hashlib
import hmac
import secrets

class HMAC:
    def __init__(self, message):
        self.secret_key = secrets.token_hex(32).upper()
        self.message = message
        self.hexdigest = self.get_hmac(self.secret_key, message).upper()
    
    def get_hmac(self, secret_key, message):
        secret_key = secret_key.encode()
        message = message.encode()
        return hmac.new(secret_key, message, hashlib.sha256).hexdigest()

