import _plotly_utils.basevalidators


class ConnectgapsValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='connectgaps', parent_name='heatmap', **kwargs
    ):
        super(ConnectgapsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            **kwargs
        )
