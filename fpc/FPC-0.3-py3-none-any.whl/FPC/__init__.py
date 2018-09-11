import datetime,builtins,platform,time
from urllib import request
IS_WIN=False if platform.system().find('Linux')>-1 else True
NOW=datetime.datetime.now().timestamp()
def print(*a,**s):builtins.print(datetime.datetime.now().strftime('%m/%d %H:%M:%S'),':',*a,**s)
def notice(x):request.urlopen(r'http://call.ff2.pw/?wc=%s&passwd=frank'%(urllib.parse.quote_plus(x)))
def rand(i=0.4,a=0.8):import random;time.sleep(random.randint(i*1000,a*1000)/1000);
def md5(x):import hashlib;hl = hashlib.md5();hl.update(x.encode('utf-8') if isinstance(x,str) else x);return hl.hexdigest();
def bin2hex(x):import binascii;return binascii.hexlify(x.encode('utf-8') if isinstance(x,str) else x);
class mysql(object):
	def __init__(self, key=127,**args):
		import pymysql
		_CONNECT_CONFIG={127:{'host':'127.0.0.1','user':'root','password':'123456','db':'localhost','charset':'utf8','cursorclass':pymysql.cursors.DictCursor}}
		connect_config = _CONNECT_CONFIG[key]
		for x in args:
			connect_config[x]=args[x]
		self.connection = pymysql.connect(**connect_config)
	def execute(self,strs):
		is_query = True if strs[:4].lower() in ['sele','show'] else False
		with self.connection.cursor() as cur:
			data=cur.execute(strs)
			if is_query : data=cur.fetchall()
		is_query or self.connection.commit()
		return data
class redis(object):
	server=False
	def __init__(self,host='127.0.0.1',db=0,port=6379,ssh_host=None,ssh_username='root',ssh_password=None):
		import redis
		if ssh_host:
			import sshtunnel
			sshtunnel.DAEMON=True
			sshtunnel.SSHTunnelForwarder.daemon_forward_servers=True
			sshtunnel.SSHTunnelForwarder.daemon_transport=True
			self.server = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=ssh_host,ssh_username=ssh_username,ssh_password=ssh_password,remote_bind_address=(host,6379))
			self.server.start()
			port=self.server.local_bind_port
		self.redis=redis.StrictRedis(host=host, port=port, db=db,decode_responses=True)
	def __getattr__(self,attr):
		return getattr(self.redis,attr)
def process(target,is_thread=True,join=False,num=1,**args):
	pros=[]
	if 'args' in args:
		args_list=args['args'] if isinstance(args['args'],list) else [args['args']]*num
	if is_thread:
		import threading
		for x in range(num):
			if 'args' in args:
				args['args']=args_list[x]
			pros.append(threading.Thread(target=target,**args))
			pros[-1].start()
	else:
		from multiprocessing import Process
		for x in range(num):
			if 'args' in args:
				args['args']=args_list[x]
			pros.append(Process(target=target,**args))
			pros[-1].start()
	if join:
		for x in range(num):
			pros[x].join()
