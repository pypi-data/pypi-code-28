import _plotly_utils.basevalidators


class ValueValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='value', parent_name='scattergl.error_x', **kwargs
    ):
        super(ValueValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            min=0,
            role='info',
            **kwargs
        )
