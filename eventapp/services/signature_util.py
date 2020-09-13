import hashlib
import hmac

def generate_signature(secretKey, payload):

    secretKey = bytes(secretKey, 'utf-8')
    payload = bytes(payload, 'utf-8')

    return hmac.new(secretKey, payload, hashlib.sha256).hexdigest()

if __name__ == '__main__':
    print(generate_signature('123','abc'))