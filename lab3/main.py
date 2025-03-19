import random
from datetime import datetime, timedelta
from Crypto.Cipher import DES

def generate_des_key():
    return random.getrandbits(64).to_bytes(8, byteorder='big')

def des_encrypt(key, data):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(data)

def des_decrypt(key, data):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(data)

def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

class KDC:
    def __init__(self):
        self.secrets = {}

    def register(self, principal, secret):
        self.secrets[principal] = secret

    def generate_ticket(self, client, service, session_key, lifetime):
        ticket_data = {
            'session_key': session_key.hex(),
            'client': client,
            'service': service,
            'lifetime': lifetime.isoformat()
        }
        ticket_str = str(ticket_data).encode()
        service_secret = self.secrets[service]
        return des_encrypt(service_secret, pad(ticket_str))

    def authenticate(self, client, lifetime):
        client_secret = self.secrets[client]
        session_key = generate_des_key()
        tgt_data = {
            'session_key': session_key.hex(),
            'client': client,
            'lifetime': lifetime.isoformat()
        }
        tgt_str = str(tgt_data).encode()
        tgt = des_encrypt(self.secrets['kdc'], pad(tgt_str))
        encrypted_response = des_encrypt(client_secret, pad(session_key + lifetime.isoformat().encode()))
        return encrypted_response, tgt

kdc = KDC()
kdc.register('client', generate_des_key())
kdc.register('service', generate_des_key())
kdc.register('kdc', generate_des_key())

client_input = input("Введите имя клиента (client): ").strip()
service_input = input("Введите имя сервиса (service): ").strip()
lifetime_input = input("Введите срок действия билета в часах: ").strip()

if client_input not in kdc.secrets:
    raise ValueError("Ошибка: Клиент не зарегистрирован в системе.")
if service_input not in kdc.secrets:
    raise ValueError("Ошибка: Сервис не зарегистрирован в системе.")
if not lifetime_input.isdigit() or int(lifetime_input) <= 0:
    raise ValueError("Ошибка: Срок действия билета должен быть положительным числом.")

lifetime = datetime.now() + timedelta(hours=int(lifetime_input))

print("\n****************************************")
print(f"Клиент отправил запрос на аутентификацию с принципалом {client_input} и запрашиваемым временем жизни {int(lifetime_input) * 3600} секунд ({lifetime_input} часов)")
print("****************************************")
response, tgt = kdc.authenticate(client_input, lifetime)

client_secret = kdc.secrets[client_input]
decrypted_response = des_decrypt(client_secret, response)
session_key = decrypted_response[:8]
print("\n****************************************")
print("Клиент получил ответ от сервера аутентификации.")
print(f"Сессионный ключ: {session_key.hex()}\n")
print("****************************************")

authenticator = {
    'client': client_input,
    'timestamp': datetime.now().isoformat()
}
authenticator_str = str(authenticator).encode()
encrypted_authenticator = des_encrypt(session_key, pad(authenticator_str))

print("****************************************")
print(f"Клиент отправляет запрос на разрешение доступа к сервису (TGS).\nПринципал сервиса: {service_input}")
print("****************************************")

service_ticket = kdc.generate_ticket(client_input, service_input, session_key, lifetime)

decrypted_ticket = des_decrypt(kdc.secrets[service_input], service_ticket)
unpadded_ticket = unpad(decrypted_ticket)
print("\n****************************************")
print("Клиент получил ответ от TGS.")
print(f"Сессионный ключ сервиса: {session_key.hex()}\n")
print("****************************************")

service_authenticator = des_encrypt(session_key, pad(authenticator_str))
print("****************************************")
print(f"Клиент отправляет запрос на разрешение доступа к сервису (TGS).")
print("****************************************")

decrypted_service_authenticator = des_decrypt(session_key, service_authenticator)
unpadded_authenticator = unpad(decrypted_service_authenticator)
print("\n****************************************")
print("Клиент получил ответ от сервиса.")
print("Полученное сообщение: It's service response\n")
print("****************************************")
