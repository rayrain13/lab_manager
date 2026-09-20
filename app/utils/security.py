import bcrypt


def hash_password(plain: str) -> str:
    """加密密码"""
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """校验密码，兼容旧版明文存储"""
    if not hashed:
        return False
    # 旧数据为明文，不以 bcrypt 前缀开头
    if not hashed.startswith('$2'):
        return plain == hashed
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except ValueError:
        return False
