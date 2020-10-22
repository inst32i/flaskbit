# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/5/29 下午11:47 
'''

import sys
import os
import multiprocessing
import gevent.monkey
gevent.monkey.patch_all()



path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)



worker_class = 'gunicorn.workers.ggevent.GeventWorker'
workers = multiprocessing.cpu_count() * 2 + 1

x_forwarded_for_header='X-FORWARDED-FOR'

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 10000
graceful_timeout = 30
keepalive=5

loglevel = 'info'

reload =True
debug = False
daemon=False

bind = "%s:%s" % ("0.0.0.0", 8000)
pidfile = '%s/run/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)
