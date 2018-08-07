"""
Author: qiacai

1. parse to get the input_type, output_type, algorithm_name for AlgorithmFactory
2. parse the input, params to run the algorithm to get the result

"""


from schematics.exceptions import ConversionError, BaseError, CompoundError, ValidationError

from ada_core.algorithms.algorithm_factory import AlgorithmFactory
from ada_core import exceptions
from ada_core.data_model.io_data_type import AlgorithmIODataType


class Handler(object):
    def __init__(self, algorithm_name: str, handler_input=None, algorithm_input_type=None, algorithm_output_type=None, params=None,
                 **kwargs):

        self.algorithm_name = algorithm_name
        self.algorithm_input_type = None
        self.algorithm_output_type = None
        self.handler_input = handler_input
        self.handler_output = None
        self.params = params

        self.algorithm_factory = AlgorithmFactory()
        self.algorithm_obj = None
        self.algorithm_meta = None
        self.algorithm_input_value = None

        if algorithm_input_type is not None:
            if AlgorithmIODataType.hasType(algorithm_input_type):
                self.algorithm_input_type = algorithm_input_type
            elif AlgorithmIODataType.hasTypeName(algorithm_input_type):
                self.algorithm_input_type = AlgorithmIODataType.getType(algorithm_input_type)
            else:
                self.algorithm_input_type = None

        if algorithm_output_type is not None:
            if AlgorithmIODataType.hasType(algorithm_output_type):
                self.algorithm_output_type = algorithm_output_type
            elif AlgorithmIODataType.hasTypeName(algorithm_output_type):
                self.algorithm_output_type = AlgorithmIODataType.getType(algorithm_output_type)
            else:
                self.algorithm_output_type = None

        if self.params is None or not isinstance(self.params, dict) or len(self.params) <= 0:
            self.params = {}

        self._handle()

    def _get_algorithm(self):

        """
        use algorithm_name, input_type, output_type to get the algorithm obj
        """
        self.algorithm_obj = self.algorithm_factory.getAlgorithm(self.algorithm_name, self.algorithm_input_type)
        #self.algorithm_obj = AlgorithmFactory.getAlgorithm(self.algorithm_name, self.algorithm_input_type)

    def _get_algorithm_meta(self):

        """
        use algorithm_name, input_type, output_type to get the algorithm meta class
        """
        algorithm_meta = self.algorithm_factory.getAlgorithmMeta(self.algorithm_name, self.algorithm_input_type)
        self.algorithm_meta = algorithm_meta()

    def _parse_handler_input(self, *args):

        pass

    def _parse_type(self):

        # get the input_type
        deduced_input_type = AlgorithmIODataType.deduceType(self.handler_input)

        if deduced_input_type is None and self.algorithm_input_type is None:
            raise exceptions.ParametersNotPassed("the algorithm_input_type is not valid")

        elif self.algorithm_input_type is not None and deduced_input_type is not None:
            if self.algorithm_input_type != deduced_input_type:
                raise exceptions.ParametersNotPassed("the algorithm_input_type not match with the deduced input type")

        elif self.algorithm_input_type is None and deduced_input_type is not None:
            self.algorithm_input_type = deduced_input_type

        # get the output_type
        deduced_output_type = self.algorithm_factory.getAlgorithmOutputType(self.algorithm_name, self.algorithm_input_type)

        if deduced_output_type is None and self.algorithm_output_type is None:
            raise exceptions.ParametersNotPassed("the algorithm_output_type is not valid")

        elif self.algorithm_output_type is None:
            self.algorithm_output_type = deduced_output_type

        elif deduced_output_type is not None and self.algorithm_output_type is not None:
            if deduced_output_type != self.algorithm_output_type:
                raise exceptions.ParametersNotPassed("the algorithm_output_type not match with the deduced input type")

    def _parse(self):

        """
        Transfer from handler input to algorithm obj acceptable input

        :return: self.algorithm_input_type, self.algorithm_output_type, self.algorithm_input
        """

        self._parse_handler_input()
        self._parse_type()

        #get the input
        input_type = self.algorithm_input_type
        type_instance = input_type()
        self.algorithm_input_value = type_instance.to_native(self.handler_input)

    def _validate_input(self):

        """

        Validate the inputs including params before calling the algorithm
        :return:
        """

        input_dict = {}
        input_dict.update(self.params)
        input_dict.update({'input_value': self.algorithm_input_value})
        self.algorithm_meta.import_data(input_dict)

        try:
            self.algorithm_meta.validate()
        except ValidationError:
            raise exceptions.ParametersNotPassed('the input and params could not pass validation')

        meta_dict = self.algorithm_meta.to_native()
        meta_dict = {key: meta_dict[key] for key in meta_dict if key not in ['alg_name', 'alg_cls', 'output_value']}
        return meta_dict

    def _validate_output(self):

        """

        Validate the output before return back
        :return:
        """
        if self.handler_output is None:
            raise exceptions.AlgorithmOutputFormatError('The output of algorithm is None')

        self.algorithm_meta.output_value = self.handler_output
        try:
            self.algorithm_meta.validate()
        except ValidationError:
            raise exceptions.ParametersNotPassed('the output could not pass validation')

    def _handle(self):
        """
        Run the handler
        :return:
        """

        self._parse()
        self._get_algorithm()
        self._get_algorithm_meta()
        self.handler_output = self.algorithm_obj.run(**self._validate_input())
        self._validate_output()

    def get_result(self):
        """
        Get the result
        :return:
        """

        if self.handler_output is None:
            self._handle()

        return getattr(self, 'handler_output', None)

    def __add__(self, other):

        if isinstance(other, Handler):
            return self.get_result() + other.get_result()
        else:
            return self.get_result() + other

    def __radd__(self, other):

        if isinstance(other, Handler):
            return self.get_result() + other.get_result()
        else:
            return self.get_result() + other

    def __sub__(self, other):

        if isinstance(other, Handler):
            return self.get_result() - other.get_result()
        else:
            return self.get_result() - other

    def __rsub__(self, other):

        if isinstance(other, Handler):
            return other.get_result() - self.get_result()
        else:
            return other - self.get_result()

    def __mul__(self, other):

        if isinstance(other, Handler):
            return self.get_result() * other.get_result()
        else:
            return self.get_result() * other

    def __rmul__(self, other):

        if isinstance(other, Handler):
            return self.get_result() * other.get_result()
        else:
            return self.get_result() * other

    def __truediv__(self, other):

        if isinstance(other, Handler):
            return self.get_result() / other.get_result()
        else:
            return self.get_result() / other

    def __rtruediv__(self, other):

        if isinstance(other, Handler):
            return other.get_result() / self.get_result()
        else:
            return other / self.get_result()

    def __floordiv__(self, other):

        if isinstance(other, Handler):
            return self.get_result() // other.get_result()
        else:
            return self.get_result() // other

    def __rfloordiv__(self, other):

        if isinstance(other, Handler):
            return other.get_result() // self.get_result()
        else:
            return other // self.get_result()

    def __mod__(self, other):

        if isinstance(other, Handler):
            return self.get_result() % other.get_result()
        else:
            return self.get_result() % other

    def __rmod__(self, other):

        if isinstance(other, Handler):
            return other.get_result() % self.get_result()
        else:
            return other % self.get_result()

    def __pow__(self, power):
        return self.get_result() ** power

    def __neg__(self):
        return -self.get_result()

    def __pos__(self):
        return +self.get_result()

    def __abs__(self):
        return abs(self.get_result())
