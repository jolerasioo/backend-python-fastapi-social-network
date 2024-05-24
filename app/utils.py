from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashing passwords
def hash_password(password: str) -> str:
    '''hash the password using bcrypt in passlib and return it as a string'''
    return pwd_context.hash(password)

# verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''verify the password using bcrypt in passlib and return a boolean'''
    return pwd_context.verify(plain_password, hashed_password)



