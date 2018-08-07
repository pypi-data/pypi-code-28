import _plotly_utils.basevalidators


class WidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='width',
        parent_name='ohlc.decreasing.line',
        **kwargs
    ):
        super(WidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='style',
            min=0,
            role='style',
            **kwargs
        )
