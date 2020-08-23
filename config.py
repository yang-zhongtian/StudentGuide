class TestConfig(object):
    SECRET_KEY = "\x18\xc0\xe6\xa4V\x84G\xb9o\xb8\xbf2\xa4\xd9\xcb_\xff\xa2\xfe\xa9l\xd8\t\xc9"
    MONGODB_URI = "mongodb://localhost:27017/stuguide"
    TEST_ACCOUNT = {"test01": "1234567890"}
    HOST = "0.0.0.0"
    PORT = 80
    DEBUG = True
    VERIFIER_AMOUNT = 5


class ProductionConfig(object):
    SERVER_NAME = "guide.hcc.io"
    MONGODB_URI = "mongodb://localhost:27017/stuguide"
    HOST = "127.0.0.1"
    PORT = 5500
    TEST_ACCOUNT = {}
    DEBUG = False
    VERIFIER_AMOUNT = 5
