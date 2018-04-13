
## 1. 采集元信息

使用`Scrapy`来采集直播间元信息，包括直播间的分类以及直播间的信息。在`metaspider/metaspider/settings.py`中更改`MongoDB`的配置：

```
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'danmu'
```

采集的元信息分为两类，正在直播的直播间，以及直播间分类。

采集正在直播的直播间信息：

```bash
$ cd metaspider
$ scrapy crawl live -L INFO
```

采集直播间分类：

```bash
$ cd metaspider
$ scrapy crawl cate -L INFO
```

## 2. 实时分析

实时分析模块需要使用到`RabbitMQ`，安装好之后需要开启以下功能：

```bash
$ rabbitmq-plugins enable rabbitmq_web_stomp
```

### 2.1 运行爬虫

在运行爬虫之前，要先修改配置文件`danmu/settings.py`

```python
FILE_STORAGE_REPOSITORY = '/path/to/store/raw_message'

LOGGING_FILE_NAME = '/path/to/store/log/danmu.log'

MQ_PARSER_ADDRESS = 'localhost' # RabbitMQ adddress 
MQ_PARSER_PORT = 5672 # RabbitMQ port
```

然后执行`scheduler.py`，需要传入两个参数，第一个是开启的工作进程的个数，第二个是需要爬取的直播间的页数。

```bash
$ export PYTHONPATH=.
$ python3 danmu/scheduler.py 8 2
```

### 2.2 运行Parser

爬取下来的原始弹幕需要经过解析才能继续使用。首先要更改`live/settings.py`中的配置

```python
LOGGING_FILE = '/path/to/log/live.log'
```

然后运行`live/consumer.py`，需要传入一个文件夹，用来存放解析后的数据

```bash
$ export PYTHONPATH=.
$ python3 live/consumer.py /path/to/repository
```

### 2.3 运行情感分析

情感分析模块使用Java语言编写，依赖如下：

运行`cn.edu.zju.douyu.mq.LiveParser`即可

### 2.4 运行Web模块

Web模块使用`Flask`编写，需要用到`Gunicorn`来执行。首先更改`site/settings.py`文件，配置`MongoDB`使之能读取到采集的元信息。

```python
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'danmu'
```

然后运行`Gunicorn`开启Web服务

```bash
$ cd site
$ export PYTHONPATH=..
$ gunicorn -w 8 -k gevent wsgi:app
```

## 3. 离线分析

离线分析模块从阿里云的`OSS`服务获取到备份的原始弹幕数据然后使用`Redis`把用户名转换成对应的ID，之后用`Spark SQL`做数据转换，最后把数据加载到数据库。


首先更改`etl/settings.py`文件中的配置

```python
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DB = 'douyu'
MYSQL_USER = 'user'
MYSQL_PASSWD = 'passwd'

LOGGING_FILE_NAME = '/path/to/log/etl.log'

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'danmu'
```

然后运行

```bash
$ export PYTHONPATH=.
$ bash etl/etl.sh repo date
```

其中`repo`是存放临时文件的文件夹，`date`是要离线解析的日期，例如`2018_03_01`

