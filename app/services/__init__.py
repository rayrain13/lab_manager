class ServiceError(Exception):
    """业务逻辑错误，由全局异常处理器转为 {code, message} 响应"""

    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)
