import _plotly_utils.basevalidators


class ArrayValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self, plotly_name='array', parent_name='histogram.error_x', **kwargs
    ):
        super(ArrayValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
