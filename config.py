# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/3/22 下午2:52
'''
class Config(object):
    """Common configuration """
    '''密码和用户名不要改动，在数据库里面请添加这个用户名和密码'''
    SQLALCHEMY_DATABASE_URI='mysql://root:mysqladmin@127.0.0.1/manifoldb'
    #SQLALCHEMY_DATABASE_URI='mysql://manifold:manifold@localhost/test'
    SECRET_KEY = 'SDQWEQWQZSDdsfwerq'
    SQLALCHEMY_TRACK_MODIFICATIONS= True


    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False  # output sql in to stderr
    SQLALCHEMY_POOL_RECYCLE = 7200  # 自动回收连接秒数，对mysql是必须的，默认是移除8小时以上的，Flask_SQL默认是2小时的
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 10000

    UPLOAD_FOLDER = ''
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx','csv','json'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentCOnfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
class ProductConfig(Config):
    """Production"""
    DEBUG=False
    SQLALCHEMY_ECHO = False

app_config={
    'development':DevelopmentCOnfig,
    'production':ProductConfig
}
if __name__ == '__main__':
    print('Hello World')
