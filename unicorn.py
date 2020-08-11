import os 
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = "unix:/var/run/studentguide.sock"
workers = multiprocessing.cpu_count() * 2 +1
max_requests = 10000
keepalive = 5
# daemon = True #服务器部署正常后开启
worker_class = "gunicorn.workers.ggevent.GeventWorker"
threads = 20
loglevel = "info"
errorlog = "log/error.log"
x_forwarded_for_header = "X_FORWARDED-FOR"

