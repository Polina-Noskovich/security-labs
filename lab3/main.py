import random
from datetime import datetime, timedelta
from Crypto.Cipher import DES

# Генерация случайного ключа DES (8 байт)
def generate_des_key():
    return random.getrandbits(64).to_bytes(8, byteorder='big')

# Функция шифрования
def des_encrypt(key, data):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(data)

# Функция дешифрования
def des_decrypt(key, data):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(data)

# Заполнение данных до кратного размера блока (64 бита)
def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

# Удаление заполнения
def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# Центр распределения ключей (KDC)
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

# Инициализация KDC
kdc = KDC()
kdc.register('client', generate_des_key())
kdc.register('service', generate_des_key())
kdc.register('kdc', generate_des_key())

# Клиентская часть
client_secret = kdc.secrets['client']
lifetime = datetime.now() + timedelta(hours=1)

# Аутентификация клиента
response, tgt = kdc.authenticate('client', lifetime)

# Дешифруем ответ для извлечения session_key
decrypted_response = des_decrypt(client_secret, response)
session_key = decrypted_response[:8]
print("Client Session Key:", session_key.hex())

# Запрос к серверу авторизации
service = 'service'
authenticator = {
    'client': 'client',
    'timestamp': datetime.now().isoformat()
}
authenticator_str = str(authenticator).encode()
encrypted_authenticator = des_encrypt(session_key, pad(authenticator_str))

# Сервер авторизации
service_ticket = kdc.generate_ticket('client', service, session_key, lifetime)

decrypted_ticket = des_decrypt(kdc.secrets['service'], service_ticket)
unpadded_ticket = unpad(decrypted_ticket)
print("Decrypted Service Ticket:", unpadded_ticket.decode())

# Клиент отправляет запрос сервису
service_authenticator = des_encrypt(session_key, pad(authenticator_str))

# Проверка на стороне сервиса
decrypted_service_authenticator = des_decrypt(session_key, service_authenticator)
unpadded_authenticator = unpad(decrypted_service_authenticator)
print("Decrypted Service Authenticator:", unpadded_authenticator.decode())
