def success(data=None, message: str = '请求成功'):
    return {'code': 200, 'message': message, 'data': data}
