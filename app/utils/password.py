import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password for storing.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Verify a stored password against one provided by user.
    """
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())
