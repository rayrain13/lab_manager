def success(data=None, message: str = '请求成功'):
    return {'code': 200, 'message': message, 'data': data}


def error(message: str = '请求失败', code: int = 400):
    return {'code': code, 'message': message}
