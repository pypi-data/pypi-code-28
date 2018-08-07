#encoding=utf8  
import inspect 
import json
import logging.config
import os 
import sys
from threading import Thread 
import threading
import time 
import uuid 
import re

import hmac
import hashlib   

from websocket import WebSocketApp      


class Protocol:
    MEMORY = 'memory'
    DISK = 'disk'
    DB = 'db'
    
    MASK_DELETE_ON_EXIT = 1 << 0
    MASK_EXCLUSIVE = 1 << 1
    
    

try:
    log_file = 'log.conf'
    if os.path.exists(log_file):
        logging.config.fileConfig(log_file)
    else:
        import os.path
        log_dir = os.path.dirname(os.path.realpath(__file__))
        log_file = os.path.join(log_dir, 'log.conf')
        logging.config.fileConfig(log_file)
except:
    logging.basicConfig(
        format='%(asctime)s - %(filename)s-%(lineno)s - %(levelname)s - %(message)s')

# support both python2 and python3
if sys.version_info[0] < 3:  
    def _bytes(buf, encoding='utf8'):
        return buf.encode(encoding) 

else:   
    def _bytes(buf, encoding='utf8'):
        return bytes(buf, encoding) 


class Dict(dict): #dynamic property support, such as d.name  
    def __getattr__(self, name): 
        if name in self: return self[name] 
    def __setattr__(self, name, value):
        self[name] = value 
    def __delattr__(self, name):
        self.pop(name, None) 
    def __getitem__(self, key):
        if key not in self: return None
        return dict.__getitem__(self, key) 


class Message(Dict): 
    
    def __init__(self, status=None, body=None, data=None):
        self.replace(data) 
        if status:
            self.status = status
            self.headers['content-type'] = 'text/html; charset=utf8'
            self.body = body
    
    def replace(self, data):
        self.clear() 
        if data and isinstance(data, (Message, dict)):
            for key in data:
                self[key] = data[key] 
        name = 'headers'
        if name not in self:
            self[name] = Dict()
        if self[name] is not Dict:
            self[name] = Dict(self[name]) 

def redirect(location):
    res = Message()
    res.status = 302
    res.headers['Location'] = location
    return res


def sign_message(api_key, secret_key, msg, encoding='utf8'):
    msg.headers.apiKey = api_key
    del msg.headers.signature
    data = json.dumps(msg, separators=(',', ':'), sort_keys=True) 
    sign = hmac.new(_bytes(secret_key,encoding), msg=_bytes(data, encoding), digestmod=hashlib.sha256).hexdigest() 
    msg.headers.signature = sign

class CountDownLatch(Dict):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()
        self.is_set = False

    def count_down(self):
        if self.is_set:
            return
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notifyAll()
            self.is_set = True
        self.lock.release()

    def wait(self, timeout=3):
        self.lock.acquire()
        if self.count > 0:
            self.lock.wait(timeout)
        self.lock.release()
     
     
class WebsocketClient(object):
    log = logging.getLogger(__name__)

    def __init__(self, address):   
        self.websocket = None 
        self.callback_table = {} 
        self.address = address 
        
        #auth
        self.api_key = None
        self.secret_key = None
        self.auth_enabled = False
        
        self.reconnect_delay = 3 
        self.auto_connect = True
        self.connect_lock = threading.Lock() 
        self.connect_active = False
        self.pending_messages = []
        
        if not address.startswith("ws://") and not address.startswith("wss://"):
            self.address = "ws://"+address 
        
        self.heartbeat_enabled = True
        self.heartbeat_interval = 30 #seconds
        self.heartbeat_msg = None
        self.heartbeat_thread = None   
          
                
        self.before_send = None    
        self.after_recv = None  
        
        def onmessage(msg):
            req = json.loads(msg)  
            req = Message(data=req)
            if self.after_recv:
                self.after_recv(req)
            
            if req.headers.id in self.callback_table:
                cb = self.callback_table[req.headers.id]
                del self.callback_table[req.headers.id]
                if cb.ondata:
                    cb.ondata(req)   
              
        self.onmessage = onmessage
        
        def _on_message(_, msg):
            if self.onmessage:
                self.onmessage(msg)  
                
        self._on_message = _on_message 
        
        def onclose(client):
            self.log.warn('Trying to reconnect in %d seconds'%self.reconnect_delay) 
            time.sleep(self.reconnect_delay) 
            client.websocket = None
            client.connect()
            
        self.onclose = onclose
        def _on_close(_):
            self.connect_active = False
            if self.onclose:
                self.onclose(self) 
                
        self._on_close = _on_close 
         
        self.onopen = None
        def _on_open(_):
            self.log.debug("Connected to %s"%self.address)  
            self.connect_active = True
            for msg in self.pending_messages:
                self.websocket.send(msg) 
            self.pending_messages = []
            
            if self.onopen: #run in new thread, prevent blocking
                t = Thread(target=self.onopen, args=(self,))
                t.setDaemon(True)
                t.start() 
                
        self._on_open = _on_open 
        
        def onerror(error):
            self.log.error(error) 
        self.onerror = onerror
        def _on_error(_, error):
            if self.onerror:
                self.onerror(error) 
        self._on_error = _on_error  
    
    def enable_auth(self, api_key=None, secret_key=None, auth_enabled=True):
        self.auth_enabled = auth_enabled
        self.api_key = api_key
        self.secret_key = secret_key
    
    def heartbeat(self):
        if not self.heartbeat_enabled: return
        if self.heartbeat_thread: return
        if not self.heartbeat_msg: return
        
        def do_heartbeat():
            while True: 
                time.sleep(self.heartbeat_interval)  
                if self.websocket:
                    try:
                        self.send(self.heartbeat_msg)
                    except:
                        pass
            
        self.heartbeat_thread = Thread(target=do_heartbeat)
        self.heartbeat_thread.setDaemon(True)
        self.heartbeat_thread.start()
    
    def connect(self): 
        with self.connect_lock:
            if self.websocket: return #connecting 

            if not self.auto_connect:
                self.onclose = None
                
            self.websocket = WebSocketApp(self.address, 
                                   on_open=self._on_open,
                                   on_message=self._on_message,
                                   on_close=self._on_close,
                                   on_error=self._on_error) 
            self.heartbeat()
            def run():
                self.websocket.run_forever()
            t = Thread(target=run)
            t.setDaemon(False)
            t.start()  
        
    
    def invoke(self, req, ondata=None, onerror=None, before_send=None, timeout=10):
        req = Message(data=req) 
        req.headers.id = str(uuid.uuid4()) 
        
        sync = None 
        
        if ondata is None:
            sync = CountDownLatch(1)
            def callback(res):
                sync.result = res
                sync.count_down() 
            ondata = callback 
        
        cb = self.callback_table[req.headers.id] = Dict()
        cb.ondata = ondata
        cb.onerror = onerror   
        
        self.send(req, before_send=before_send)  
        
        if sync:
            sync.wait(timeout) 
            return sync.result 
    
    def send(self, data, before_send=None):
        handler = before_send or self.before_send
        if handler:
            handler(data)
            
        if self.auth_enabled:
            if self.api_key is None:
                raise 'missing api_key for auth'
            if self.secret_key is None:
                raise 'missing secret_key for auth'
            sign_message(self.api_key, self.secret_key, data)
            
        msg = json.dumps(data)
        
        if not self.connect_active:
            self.pending_messages.append(msg)
            self.connect()
            return
            
        self.websocket.send(msg) 
        
    def close(self): 
        self.onclose = None 
        if self.websocket:
            self.websocket.close()
        self.websocket = None
        self.connect_active = False


class MqClient(WebsocketClient):
    log = logging.getLogger(__name__)

    def __init__(self, address):  
        WebsocketClient.__init__(self, address)  
        self.handler_table = {} #mq=>{channel=>handler}
        
        self.heartbeat_msg = Message()
        self.heartbeat_msg.headers.cmd = 'ping' 
        
        def onmessage(msg):
            req = json.loads(msg)  
            req = Message(data=req)
            if self.after_recv:
                self.after_recv(req)
            
            if req.headers.id in self.callback_table:
                cb = self.callback_table[req.headers.id]
                del self.callback_table[req.headers.id]
                if cb.ondata:
                    cb.ondata(req)  
                return 
             
            mq, channel = req.headers.mq, req.headers.channel
            if mq not in self.handler_table:
                self.log.warn("Missing handler for mq=%s, msg=%s"%(mq, msg))
                return
            handlers = self.handler_table[mq]
            if channel not in handlers:
                self.log.warn("Missing handler for mq=%s, channel=%s"%(mq,channel))
                return
            
            mq_handler = handlers[channel]
            mq_handler.handler(req)   
            
            #update window if limit reached
            window = req.headers.window
            if window is not None and int(window) <= mq_handler.window/2:
                sub = Message()
                sub.headers.cmd = 'sub'
                sub.headers.mq = mq
                sub.headers.channel = channel
                sub.headers.window = mq_handler.window 
                sub.headers.ack = 'false'
                self.send(sub, mq_handler.before_send)       
                    
        self.onmessage = onmessage
          
    
    def add_mq_handler(self, mq=None, channel=None, handler=None, window=1, before_send=None):
        if mq not in self.handler_table:
            self.handler_table[mq] = {}
        
        mq_handler = Dict()
        mq_handler.handler = handler
        mq_handler.window = window
        mq_handler.before_send = before_send
        self.handler_table[mq][channel] = mq_handler
        
  

#===================================RPC======================================
'''
path -- url path
method -- http method: GET|POST etc.
'''
def route(path=None, method=None):
    def func(fn):
        if path:
            fn._path = path
        if method: 
            fn._method = method 
        return fn
    return func

def exclude():
    def func(fn): 
        fn._exclude = True 
        return fn
    return func
'''
inject request object for method
'''
def inject():
    def func(fn): 
        fn._inject = True 
        return fn
    return func

def add_filter(filter_fn=None):
    def func(fn):
        if filter_fn:
            fn._filter = filter_fn 
        return fn
    return func

def join_path(*args):  
    p = '/'.join(args) 
    p = '/'+p
    p = re.sub(r'[/]+','/', p)
    if len(p) > 1 and p.endswith('/'):
        p = p[0:-1]
    return  p  


class RpcClient(WebsocketClient): 
    def __init__(self, address, url_prefix='', timeout=10):
        WebsocketClient.__init__(self, address)
        self.timeout = timeout #10s for sync invoke   
        self.heartbeat_msg = Message()
        self.heartbeat_msg.headers.cmd = 'ping'
        self.url_prefix = url_prefix   

    def invoke(self, method='', params=[], url_prefix='', ondata=None, onerror=None, timeout=10):
        req = Message()
        req.url = join_path(url_prefix, method)
        req.body = params  
        
        sync = None 
        
        if ondata is None:
            sync = CountDownLatch(1)
            def callback(res):
                sync.result = res
                sync.count_down() 
            ondata = callback
            
        def onmessage(msg):
            if msg.status == 200:
                ondata(msg.body)
            else:
                e = Exception(msg.body) 
                if onerror:
                    onerror(e)
                else:
                    if sync: 
                        sync.error = e 
                        sync.count_down()
        
        WebsocketClient.invoke(self, req, ondata=onmessage, onerror=onerror)
        if sync:
            sync.wait(timeout)
            if sync.error:
                raise sync.error
            return sync.result 
    
    def __getattr__(self, name):    
        return self._invoker(name) 

    def _invoker(self, module): 
        url_prefix = join_path(self.url_prefix, module)
        return RpcInvoker(client=self, url_prefix=url_prefix, timeout=self.timeout) 
    
class RpcInvoker:
    def __init__(self, client=None, url_prefix='', method='', timeout=10):
        self.client = client 
        self.url_prefix = url_prefix
        self.method = method
        self.timeout = timeout 
    
    def __getattr__(self, name):    
        return RpcInvoker(client=self.client, url_prefix=self.url_prefix, method=name, timeout=self.timeout)
    
    def __call__(self, *args, **kv_args):  
        return self.client.invoke(method=self.method, params=args, url_prefix=self.url_prefix, timeout=self.timeout,**kv_args)    
    


    
class RpcInfo:
    RpcInfoTemplate = '''
<html><head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<title>%s Python</title>      
%s
</head>
<body>    
<script>  
var rpc; 
function init(){
    rpc = new RpcClient(null,'%s'); 
} 
</script> 
<script async src="https://unpkg.com/zbus/zbus.min.js" onload="init()">
</script>    

<div>  
<div class="url">
    <span>URL=%s[module]/[method]/[param1]/[param2]/...</span> 
</div>
<table class="table"> 
<thead>
<tr class="table-info">  
    <th class="urlPath">URL Path</th>
    <th class="returnType">Return Type</th> 
    <th class="methodParams">Method and Params</th>  
</tr> 
<thead> 
<tbody> 
%s 
</tbody> 
</table> </div> </body></html>
'''

    RpcStyleTemplate = '''
<style type="text/css">
body {
    font-family: -apple-system,system-ui,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #292b2c;
    background-color: #fff;
    margin: 0px;
    padding: 0px;
}
table {  background-color: transparent;  display: table; border-collapse: separate;  border-color: grey; }
.table { width: 100%; max-width: 100%;  margin-bottom: 1rem; }
.table th {  height: 30px; }
.table td, .table th {    border-bottom: 1px solid #eceeef;   text-align: left; padding-left: 16px;} 
th.urlPath {  width: 10%; }
th.returnType {  width: 10%; }
th.methodParams {   width: 80%; } 
td.returnType { text-align: right; }
thead { display: table-header-group; vertical-align: middle; border-color: inherit;}
tbody { display: table-row-group; vertical-align: middle; border-color: inherit;}
tr { display: table-row;  vertical-align: inherit; border-color: inherit; }
.table-info, .table-info>td, .table-info>th { background-color: #dff0d8; }
.url { margin: 4px 0; padding-left: 16px;}
</style>
'''

    RpcMethodTemplate = '''
<tr> 
    <td class="urlPath"> <a href="%s"/>%s</a> </td>
    <td class="returnType"></td>
    <td class="methodParams">
        <code><strong><a href="%s"/>%s</a></strong>(%s)</code>     
    </td>  
</tr> 
'''

    def __init__(self, rpc_processor, url_prefix='/'):
        self.rpc_processor = rpc_processor
        self.url_prefix = url_prefix #golbal url_prefix
    
    @route('/')
    def index(self):
        res = Message()
        res.status = 200 
        res.headers['content-type'] = 'text/html; charset=utf-8' 
        
        rpc = self.rpc_processor
        info = ''  
        for urlpath in rpc.urlpath2method:
            m = rpc.urlpath2method[urlpath].info
            if not m.doc_enabled: continue 
            link = join_path(self.url_prefix, urlpath)
            args = ', '.join(m.params)
            info += RpcInfo.RpcMethodTemplate%(link, link, link, m.method , args)
         
        res.body = RpcInfo.RpcInfoTemplate%(self.url_prefix, RpcInfo.RpcStyleTemplate, self.url_prefix, self.url_prefix, info)
           
        return res  

class RpcProcessor:
    log = logging.getLogger(__name__) 
    
    def __init__(self):  
        self.doc_url_prefix = '/doc'
        self.doc_enabled = True
        
        self.urlpath2method = Dict() 
        self.req_filter = None
        self.error_pages = Dict() # status=>page generator 

    def mount(self, prefix, service, doc_enabled=True): 
        if inspect.isclass(service):
            service = service()  
        
            
        methods = inspect.getmembers(service, predicate=inspect.ismethod)
        for method in methods:
            method_name = str(method[0])
            if method_name.startswith('_'):
                continue 
            
            url_path = join_path(prefix, method_name)
            http_method = None
            req_filter = None
            req_inject = False
            exclude = False
            if hasattr(method[1], '_path'):
                url_path = join_path(prefix, getattr(method[1], '_path')) 
            if hasattr(method[1], '_method'):
                http_method = getattr(method[1], '_method')  
            if hasattr(method[1], '_filter'):
                req_filter = getattr(method[1], '_filter')  
            if hasattr(method[1], '_inject'):
                req_inject = getattr(method[1], '_inject')  
            if hasattr(method[1], '_exclude'):
                exclude = getattr(method[1], '_exclude')  
            
            if url_path in self.urlpath2method:
                self.log.warn('{URL=%s, method=%s} duplicated' % (url_path, method_name))   
            if exclude: 
                continue
                
            params = inspect.getargspec(method[1]) 
            info = Dict()
            info.url_path = url_path
            info.method = method_name
            info.http_method = http_method
            info.params = params.args[1:] 
            info.defaults = params.defaults or {}
            info.doc_enabled = doc_enabled
            
            method_instance = Dict()
            method_instance.method = method[1]
            method_instance.params = params.args[1:]
            method_instance.info = info  
            method_instance.filter = req_filter
            method_instance.inject = req_inject
            self.urlpath2method[url_path] = method_instance # (method[1], params.args, info) 
             

    def mount_doc(self, url_prefix='/'):  
        if self.doc_enabled: 
            if self.doc_url_prefix in self.urlpath2method: return 
            self.mount(self.doc_url_prefix, RpcInfo(self, url_prefix), doc_enabled=False) 
     
    
    def _reply(self, res, status, msg=None, request=None):
        res.status = status
        res.headers['content-type'] = 'text/html; charset=utf8'
        fn = self.error_pages[status]
        if fn:
            try:
                res.body = fn(request=request, msg=msg)
            except Exception as e:
                print(e)
                res.body = '%s: %s'%(status, msg)
        else:
            if msg:
                res.body = '%s: %s'%(status, msg)
            else: 
                res.body = 'Status=%s: Missing error page?'%status
    
    def set_error_page(self, status, page_generator):
        fn = page_generator
        if isinstance(fn, str):
            def error_page(**kvargs):
                return page_generator
            fn = error_page
        self.error_pages[status] = fn
     
    def _parse_params(self, s):
        bb = s.split('?')
        path = bb[0]
        qs = None
        if len(bb) > 1:
            qs = ''.join(bb[1:])
        bb = path.split('/') 
        res = [b for b in bb if b != '']
        query_map = {}
        if qs:
            data = {}
            bb = qs.split('&') 
            for kv in bb:
                if kv == '': continue
                kk = kv.split('=')
                key = kk[0]
                if len(kk) > 0:
                    val = ''.join(kk[1:])
                data[key] = val
            if len(data) > 0:
                query_map = data
        return (res, query_map)
    
    def parse_request(self, req, res):
        url = req.url 
        query_map = {}
        if req.body:
            content_type = req.headers['content-type']
            if content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
                if isinstance(req.body, str): 
                    req.body = json.loads(req.body)
                if 'files' in req.body and len(req.body['files']) == 0:
                    if 'attributes' in req.body:
                        query_map = req.body['attributes'] #form attributes data as query params
                        req.body = []
                else:
                    req.body = [req.body] 
            elif isinstance(req.body, str): 
                req.body = json.loads(req.body)
            elif isinstance(req.body, list):
                pass 
            else:
                res.body = [res.body] 
                
        params = req.body or []
        
        length = 0
        target_method = None
        target_path = None
        for path in self.urlpath2method: 
            if url == path or url.startswith('%s/'%path) or url.startswith('%s?'%path):
                if length < len(path):
                    length = len(path)
                    target_path, target_method = (path, self.urlpath2method[path])
        
        if target_method is None:
            self._reply(res, 404, msg='Url=%s Not Found'%(url), request=req)  
            return (None, None, None) 
        method_info = target_method.info
        http_method = method_info.http_method
        if http_method:
            if req.method is None:
                self._reply(res, 405, msg='Method(%s) required'%(http_method), request=req)  
                return (None, None, None) 
            if http_method.lower() != req.method.lower():
                self._reply(res, 405, msg='%s Not Allowed'%(req.method), request=req)  
                return (None, None, None)
         
        if params == [] and len(query_map)==0:
            params, query_map = self._parse_params(url[len(target_path):]) 
        return (target_method, params, query_map)
    
    def normalize_params(self, req, res, target_method, params, query_map, kvargs): 
        url = req.url
        method_info = target_method.info
        total_params = len(target_method.params) 
        kvargs_len = len(method_info.defaults)
        args_len = total_params - kvargs_len 
        
        if len(params) == 0 and total_params == 1 and len(query_map) > 0: 
            params.append(Dict(query_map)) 
            return True
         
        if len(params) > total_params: 
            params_str = ','.join(method_info.params)
            self._reply(res, 400, msg='URL=%s, Method=%s, Params=(%s), Bad Request'%(url, method_info.method, params_str), request=req)  
            return False
             
        if len(query_map) == 0 and len(params) < args_len:
            params_str = ','.join(method_info.params)
            self._reply(res, 400, msg='URL=%s, Method=%s, Params=(%s), Bad Request'%(url, method_info.method, params_str), request=req)  
            return False
        i = len(params)
        while i<args_len: #take args from kvargs
            arg_name = method_info.params[i] 
            if arg_name not in query_map: 
                params_str = ','.join(method_info.params)
                self._reply(res, 400, msg='URL=%s, Method=%s, Params=(%s), Missing value for key=%s'%(url, method_info.method, params_str, arg_name), request=req)  
                return 
            else:
                params.append(query_map[arg_name])
            i += 1 
        
        i = len(params) 
        while i<total_params:
            arg_name = method_info.params[i]
            if arg_name not in query_map:
                kvargs[arg_name] = method_info.defaults[i-args_len]
            else:
                kvargs[arg_name] = query_map[arg_name]
            i += 1 
        return True
    
    '''
    query_map: query string or form body parsed dictionary
    '''
    def process(self, req, res):   
        if self.req_filter:
            do_next = self.req_filter(req, res) 
            if not do_next:
                return
        url = req.url 
        if not url:
            self._reply(res, 400, msg='Missing url in request', request=req)  
            return   
        
        target_method, params, query_map = self.parse_request(req, res)
        if not target_method: return
        
        method = target_method.method
        method_info = target_method.info  
        try:    
            kvargs = {}
            req_inject = target_method.inject
            if req_inject:
                params.append(req) #last parameter as request context 
                
            ok = self.normalize_params(req, res, target_method, params, query_map, kvargs) 
            if not ok: return
            
            req_filter = target_method.filter
            if req_filter:
                req.ctx = Dict()
                req.ctx.method = method_info.method
                req.ctx.params = params
                
                do_next = req_filter(req, res)
                if not do_next:
                    return 
                
            result = method(*params, **kvargs)
            if isinstance(result, Message):
                res.replace(result)
            else:
                res.headers['content-type'] = 'application/json; charset=utf8'
                res.body = result 
            if not res.status:
                res.status = 200
        except Exception as e:
            self._reply(res, 500, msg=str(e), request=req) 
            return  

    def __call__(self, *args):
        return self.process(*args)   
    
class RpcServer: 
    log = logging.getLogger(__name__) 
    def __init__(self, processor): 
        self.mq_server_address = None
        self.mq = None
        self.mq_type = None
        self.mq_mask = None
        self.channel = None  
        self.heartbeat_interval = 30
        self.use_thread = False 
        
        self.auth_enabled = False
        self.api_key = None
        self.secret_key = None
        
        self.processor = processor 
        
        self._mqclient = None 
        
    
    def enable_auth(self, api_key=None, secret_key=None, auth_enabled=True):
        self.auth_enabled = auth_enabled
        self.api_key = api_key
        self.secret_key = secret_key
    
    def start(self):
        if self.mq_server_address is None:
            raise Exception("missing mq_server_address")
        if self.mq is None:
            raise Exception("missing mq")
        if self.channel is None:
            self.channel = self.mq 
        
        self.processor.mount_doc(join_path(self.mq))
            
        client = self._mqclient = MqClient(self.mq_server_address)
        client.auth_enabled = self.auth_enabled
        client.api_key = self.api_key
        client.secret_key = self.secret_key
        
        def create_mq(client):
            def sub_cb(res):
                if res.status != 200:
                    self.log.error(res)
                else:
                    self.log.info(res)
            def create_cb(res):
                if res.status != 200:
                    self.log.error(res)
                else:
                    self.log.info(res)
                msg = Message()
                msg.headers.cmd = 'sub'
                msg.headers.mq = self.mq
                msg.headers.channel = self.channel    
                client.invoke(msg, ondata=sub_cb)  
                
            msg = Message()
            msg.headers.cmd = 'create'
            msg.headers.mq = self.mq
            msg.headers.mqType = self.mq_type
            msg.headers.mqMask = self.mq_mask
            msg.headers.channel = self.channel  
            
            client.invoke(msg, ondata=create_cb) 
              
        
        url_prefix = join_path(self.mq)
        def _rpc_handler(client, processor, req):
            if req.status == 404:
                create_mq(client)
                return   
             
            if req.url and req.url.startswith(url_prefix):
                req.url = req.url[len(url_prefix):]
                req.url = join_path('/', req.url)
            
            res = Message() 
            msgid = req.headers.id
            target = req.headers.source
            try:
                processor(req, res)  
            except Exception as e:
                self.log.error(e)
                res.status = 500
                res.headers['content-type'] = 'text/plain; charset=utf8'
                res.body = str(e)
            
            res.headers.cmd = 'route'
            res.headers.id = msgid 
            res.headers.target = target
            
            client.send(res)
            
        def rpc_handler(req):
            if self.use_thread:
                t = Thread(target=_rpc_handler, args=(client, self.processor, req))
                t.start()
            else:
                _rpc_handler(client, self.processor, req)
            
        client.add_mq_handler(mq=self.mq, channel=self.channel, handler=rpc_handler)
        client.onopen = create_mq 
        client.connect()  
         
        
    def close(self):
        if self._mqclient:
            self._mqclient.close()
            self._mqclient = None  

class StaticResource(object):  
    def __init__(self, base_dir=None, cache_enabled=False, mime_types_fn=None):
        self.base_dir = base_dir
        self.cache_enabled = cache_enabled 
        self.file_table = {}
        self._mime_type_fn = mime_types_fn  
        self._mime_types = {  
            "js": "application/javascript", 
            "json": "application/json",
            "css": "text/css",
            "htm": "text/html", 
            "html": "text/html",
            "svg": "image/svg+xml",
            "gif": "image/gif", 
            "jpeg": "image/jpeg", 
            "jpg": "image/jpg",
            "ico": "image/x-icon",
            "png": "image/png",
            "pdf": "application/pdf",   
            "zip": "application/zip",   
            "ttf": "application/x-font-ttf", 
            "eot": "font/opentype" 
        }
        def mime_type(ext):
            if self._mime_type_fn:
                res = self._mime_type_fn(ext)
                if not res: return res
            if ext in self._mime_types:
                return self._mime_types[ext]
            return None
        self.mime_type_fn = mime_type
    
    @route('/')
    def file(self, file_name):
        file_path = file_name
        if self.base_dir:
            file_path = os.path.join(self.base_dir, file_name)
        if self.cache_enabled and file_path in self.file_table:
            file_content = self.file_table[file_path]
        else:
            try:
                with open(file_path) as f:
                    file_content = f.read() 
                    self.file_table[file_path] = file_content 
            except:
                return Message(404, 'File=%s Not Found'%file_name)
                
        res = Message()
        res.status = 200
        content_type = None
        idx = file_name.rfind('.')
        if idx != -1:
            ext = file_name[idx+1:]
            content_type = self.mime_type_fn(ext)
        if not content_type:
            content_type = 'text/plain'
        
        res.headers['content-type'] = '%s; charset=utf8'%content_type
        res.body = file_content
        
        return res

class Template(object): 
    def __init__(self, base_dir=None, cache_enabled=False, ctx=None):
        self.base_dir = base_dir
        self.cache_enabled = cache_enabled
        from jinja2 import Template as jinjaTempalte
        self.jinjaTemplate = jinjaTempalte
        self.template_table = {}
        self.ctx = ctx
    
    def render(self, tpl_file, **kvargs):
        if self.base_dir:
            tpl_file = os.path.join(self.base_dir, tpl_file)
        if self.cache_enabled and tpl_file in self.template_table:
            tpl = self.template_table[tpl_file]
        else:
            with open(tpl_file, encoding='utf8') as f:
                content = f.read()
                tpl = self.jinjaTemplate(content)
                self.template_table[tpl_file] = tpl
        
        if self.ctx and 'ctx' not in kvargs:
            kvargs['ctx'] = self.ctx
        
        s = tpl.render(**kvargs) 
        res = Message()
        res.status = 200
        res.headers['content-type'] = 'text/html; charset=utf8'
        res.body = s
        
        return res
    
    def __call__(self, tpl_file, **kvargs):
        return self.render(tpl_file, **kvargs)
        
 

class Controller: 
    def __init__(self, db=None, template=None):
        from sqlalchemy.orm import sessionmaker 
        self.sessionmaker = sessionmaker
        from sqlalchemy.sql import text  
        self.text = text
        
        self.template = template
        self.db = db 
        if self.db:
            self.Session = sessionmaker(bind=self.db) 
        if self.template:
            self.url_prefix = self.template.ctx['url_prefix'] or '' 
        
    @exclude()    
    def redirect(self, location):
        return redirect(join_path(self.url_prefix, location))
    @exclude()    
    def render(self, tpl_file, **kvargs): 
        return self.template.render(tpl_file, **kvargs)
    @exclude() 
    def query(self, sql, converter=None, **kvargs): 
        with self.db.connect() as con:
            sql = self.text(sql)
            rs = con.execute(sql, **kvargs)
            def c(row):
                if not converter: return Dict(row)
                return converter(row)
            return [c(row) for row in rs]  
    @exclude()     
    def execute_sql(self, sql, **kvargs): 
        with self.db.connect() as con:
            sql = self.text(sql)
            return con.execute(sql, **kvargs)
    @exclude()     
    def query_one(self, sql, converter=None, **kvargs): 
        res = self.query(sql, converter, **kvargs)
        if len(res) > 0: return res[0]
        
    @exclude() 
    def save(self, m): 
        sess = self.Session()
        sess.merge(m) 
        sess.commit()
        sess.close()     
        

def start_service(rpc_processor, server_address='localhost:15555', url_prefix='/', use_thread=True):
    server = RpcServer(rpc_processor)  
    server.mq_server_address = server_address
    server.mq = url_prefix
    server.use_thread = use_thread
    server.mq_mask = Protocol.MASK_DELETE_ON_EXIT#delete on exit
    server.start()   