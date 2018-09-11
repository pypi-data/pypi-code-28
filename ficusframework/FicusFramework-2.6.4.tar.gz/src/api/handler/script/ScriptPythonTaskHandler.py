import logging
import threading

from api.handler.ICacheAbleHandler import ICacheAbleHandler
from api.handler.ITaskHandler import ITaskHandler
from api.handler.outputer.ISimpleOutputer import ISimpleOutputer
from api.handler.script import ScriptPythonFactory
from api.model.FdInputPipe import FdInputPipe
from api.model.ResultVO import *
from client import ComputeExecutionClient

log = logging.getLogger('Ficus')

class ScriptPythonTaskHandler(ITaskHandler,ISimpleOutputer, ICacheAbleHandler):
    """
    Python脚本的执行器
    """

    # 由于这个的实现有可能是 单例的,所以要使用ThreadLocal
    __code_local_host = threading.local()
    __execution_message_local = threading.local()

    def __init__(self, job_id, update_time, script_source):
        self.job_id = job_id
        self.update_time = update_time
        self.script_source = script_source

    def update_time(self):
        return self.update_time

    def execute(self, params):
        """
        执行Python脚本的处理
        :param params:
        :return:
        """
        if params is None or len(params) == 0 or ("site_" not in params) or ("projectCode_" not in params) or (
                "code_" not in params):
            # 不存在ce的信息,没法执行
            return ResultVO(FAIL_CODE, "执行失败,没有ComputeExecute的信息")

        # 这里动态的加载script源文件
        sampleScriptCE = ScriptPythonFactory.load_instance(f"ScriptPython{self.job_id}",self.script_source)

        # 获取ce定义
        dataComputeExecution = ComputeExecutionClient.get(params["site_"], params["projectCode_"], params["code_"])

        resultList = None
        try:
            self.set_local_code(f"{dataComputeExecution.site}_{dataComputeExecution.projectCode}_{dataComputeExecution.code}")
            resultList = sampleScriptCE.do_compute(FdInputPipe(dataComputeExecution.sourceFdCodes),params)
        except Exception as e:
            log.error(f"{dataComputeExecution.site}_{dataComputeExecution.projectCode}_{dataComputeExecution.code} 接收到消息执行失败,{str(e)}")
            return
        finally:
            self.clear_local_code()

        if  resultList is None or len(resultList)==0:
            # 搞完了,没的结果,不处理
            return SUCCESS

        # 有结果,就需要从crawl的配置中找到目标的fd,然后调用fd的接口进行保存
        outputFdCodes = dataComputeExecution.outputFdCodes

        try:
            self.send_output_result(dataComputeExecution.code,resultList,outputFdCodes)
        except Exception as e:
            log.error(f"{dataComputeExecution.site}_{dataComputeExecution.projectCode}_{dataComputeExecution.code} 发送结果数据失败,{str(e)}")

        return SUCCESS


    def kill(self):
        ScriptPythonFactory.destroy_instance(f"ScriptPython{self.job_id}")

    def get_execution_message_cache(self):
        """
        返回message_cache
        :return:
        """
        return self.__execution_message_local.content

    def get_code_thread_local(self):
        return self.__code_local_host