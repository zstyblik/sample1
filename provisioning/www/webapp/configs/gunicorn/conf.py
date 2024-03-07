name = "webapp"
bind = "0.0.0.0:3031"
user = "www-data"
group = "www-data"
max_requests = 1000
max_requests_jitter = 3000
loglevel = "info"
errorlog = "-"
accesslog = "-"
workers = 2
forwarded_allow_ips = "*"
# Which headers signal request is over HTTPS
secure_scheme_headers = {"X-FORWARDED-PROTO": "https"}
access_log_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # noqa
