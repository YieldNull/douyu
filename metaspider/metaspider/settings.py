BOT_NAME = 'metaspider'

SPIDER_MODULES = ['metaspider.spiders']
NEWSPIDER_MODULE = 'metaspider.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8

# DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 4
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
}

USER_AGENT_LIST = 'useragents.txt'
REFERER_ENABLED = False

# SPIDER_MIDDLEWARES = {
#    'metaspider.middlewares.MetaspiderSpiderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    'metaspider.pipelines.MetadataPipeline': 300,
}

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'danmu'
