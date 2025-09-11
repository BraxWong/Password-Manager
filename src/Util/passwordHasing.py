import bcrypt

def encode_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes,salt)
    return hash.decode('utf-8')

def check_password(userPassword,dbPassword):
    return bcrypt.checkpw(
        userPassword.encode('utf-8'),
        dbPassword.encode('utf-8')
    )