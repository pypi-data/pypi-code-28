from abc import abstractmethod

from api.model.FdInputPipe import FdInputPipe

class ISampleScriptCE:
    """
    Python脚本式的CE的基类
    """

    @abstractmethod
    def do_compute(self,source_fds:FdInputPipe, params:dict):
        pass