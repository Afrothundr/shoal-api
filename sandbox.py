import pocketcasts

pocket = pocketcasts.Pocketcasts('branford.harris@outlook.com', password='88elves')

print(pocket.get_listening_history());

# from cryptography.fernet import Fernet
# from api.settings import FERNET_KEY

# def encrypt(message: bytes, key: bytes) -> bytes:
#     return Fernet(FERNET_KEY).encrypt(message)

# def decrypt(token: bytes, key: bytes) -> bytes:
#     return Fernet(FERNET_KEY).decrypt(token)

# message = 'John Doe'
# token = encrypt(message.encode(), FERNET_KEY)
# print(token)
# print (decrypt(token, FERNET_KEY).decode())

