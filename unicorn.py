import os 
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = "127.0.0.1:5500"#"unix:/var/run/studentguide.sock"
workers = multiprocessing.cpu_count() * 2 +1
max_requests = 10000
worker_connections = 10000
keepalive = 5
worker_class = "gunicorn.workers.ggevent.GeventWorker"
threads = 20
loglevel = "info"
errorlog = "log/error.log"
x_forwarded_for_header = "X_FORWARDED-FOR"

