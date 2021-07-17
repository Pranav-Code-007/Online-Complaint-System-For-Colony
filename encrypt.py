from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)


def encrypt(message):
    return fernet.encrypt(message.encode())


def decrypt(message):
    return fernet.decrypt(message.decode())
