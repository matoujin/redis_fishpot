import json
import time
import os
import datetime
import re
import twisted.python.logfile
from configparser import SafeConfigParser

class JsonLog(object):
    def __init__(self):
        dire = os.path.dirname('./log/')
        self.outfile = twisted.python.logfile.DailyLogFile("redis.log", dire, defaultMode=0o664)

    def get_log(self, command, rhost, rport):
        data = {}
        # safeconfigparser used to read conf-file
        parse = SafeConfigParser()
        parse.read("redis.conf")
        dst_ip = parse.items("IP")
        # timestamp -> data
        data['timestamp'] = datetime.datetime.fromtimestamp(time.time()).isoformat()
        data['dst_ip'] = dst_ip[0][1]
        data['dst_port'] = 6379
        data['src_ip'] = rhost
        data['src_port'] = rport
        data['command'] = command
        line = json.dumps(data)
        self.outfile.write(line+"\n")
        self.outfile.flush()