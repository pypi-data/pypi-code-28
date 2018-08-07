import _plotly_utils.basevalidators


class ValueminusValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='valueminus',
        parent_name='histogram.error_y',
        **kwargs
    ):
        super(ValueminusValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            min=0,
            role='info',
            **kwargs
        )
