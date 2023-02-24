import hashlib
import base64
import hmac

from dao.user import UserDAO
from config import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, user_name):
        return self.dao.get_by_username(user_name)

    def create(self, user_data):
        user_data['password'] = self.generate_password(user_data['password'])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data['password'] = self.generate_password(user_data['password'])
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password: str):
        """ Возвращает паророль загифрованный вметодом sha256 в виде бинарного кода"""
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        # возвращает пароль в виде строки
        return base64.b64encode(hash_digest)

    def compare_password(self, password_hash, other_password) -> bool:
        decoding_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoding_digest, hash_digest)
