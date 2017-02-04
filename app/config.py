import os
import ConfigParser
from itertools import chain

BRAND_NAME = 'Simplesurance Text search service'

APP_ENV = os.environ.get('APP_ENV') or 'local'  # or 'prod' to load production
INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../conf/{}.ini'.format(APP_ENV))

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(INI_FILE)
#POSTGRES = CONFIG['postgres']
#if APP_ENV == 'dev' or APP_ENV == 'live':
    #DB_CONFIG = (POSTGRES['user'], POSTGRES['password'], POSTGRES['host'], POSTGRES['database'])
    #DATABASE_URL = "postgresql+psycopg2://%s:%s@%s/%s" % DB_CONFIG
#else:
    #DB_CONFIG = (POSTGRES['host'], POSTGRES['database'])
    #DATABASE_URL = "postgresql+psycopg2://%s/%s" % DB_CONFIG

#DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
#DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG.get("logging", "level")
