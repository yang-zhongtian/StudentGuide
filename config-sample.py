class TestConfig(object): # 测试服务器
    SECRET_KEY = "" # 测试秘钥
    MONGODB_URI = "" # 数据库
    TEST_ACCOUNT = {} # 测试账号（用户名：密码）
    HOST = "0.0.0.0"
    PORT = 80
    DEBUG = True
    VERIFIER_AMOUNT = 5 # 弹幕审核人员数量
    ONLY_ALLOW_DANMU = False # 只允许查看弹幕页


class ProductionConfig(object): # 生产服务器
    SERVER_NAME = "" # 生产域名
    SECRET_KEY = "" # 生产秘钥
    MONGODB_URI = "" # 生产数据库，例子：mongodb://localhost:27017/stuguide
    HOST = "127.0.0.1"
    PORT = 5500
    TEST_ACCOUNT = {}
    DEBUG = False
    VERIFIER_AMOUNT = 5 # 弹幕审核人员数量
    ONLY_ALLOW_DANMU = False # 只允许查看弹幕页
