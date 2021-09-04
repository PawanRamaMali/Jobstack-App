from passlib.context import CryptContext
from passlib.utils.decor import deprecated_function

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwt_context.verify(plain_password,hashed_password)

    @staticmethod
    def get_password_hash(plain_password):
        return pwt_context.hash(plain_password)