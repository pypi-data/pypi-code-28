"""
Author: qiacai
"""


__all__ = ['naive_algorithm', 'binary_num1num_judge_algorithms', 'binary_ts1num2ts_calculate_algorithms', 'unary_ts2num_calculate_algorithms', 'unary_ts2ts_calculate_algorithms',
           'unary_judge_algorithms']


class Algorithm(object):
    """
    Base class for Algorithm
    """

    def __init__(self, class_name):
        self.class_name = class_name
        # self.input_type = None
        # self.output_type = None
        # self.name = 'algorithm'

    def _run_algorithm(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        return self._run_algorithm(*args, **kwargs)

    # def getName(self):
    #     return self.name
    #
    # def getClass(self):
    #     return self.class_name
    #
    # def getInputType(self):
    #     return self.input_type
    #
    # def getOutputType(self):
    #     return self.output_type