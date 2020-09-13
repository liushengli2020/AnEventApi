class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True

class DevConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.dev.db'
    testing = True
    debug = True

class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'
    testing = False
    debug = False
