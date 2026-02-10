from auth.user_db import create_user, get_user
from auth.password_utils import hash_password, verify_password

def signup(name, email, password):
    hashed = hash_password(password)
    create_user(name, email, hashed)

def login(email, password):
    user = get_user(email)
    if not user:
        return False

    stored_hash = user[3]
    return verify_password(password, stored_hash)
